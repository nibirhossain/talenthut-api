from rest_framework import serializers
from django.db import transaction
from django.utils import timezone
from ..models import RecruiterActivity, RecruiterActivityHistory
from .serializers import RecruiterEventSerializer
from .recruiter import RecruiterSerializer
from .serializers import TalentMiniSerializer
from ..models import RecruiterEvent


# The serializer used to list recruiter activities with minimal fields
class RecruiterActivityMiniSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecruiterActivity
        fields = '__all__'


class FilteredListSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        recruiter_events = RecruiterEvent.objects.all()
        temp_data = []
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        if user and getattr(request.user, 'recruiter', False):
            data = data.filter(recruiter__id=user.recruiter.id)

            # ........................................................................... #
            # CASE 1 |     X    |          X           |     X    |     X    |     X    | #
            # ........................................................................... #
            # CASE 2 |     X    | Send Contact Request |     X    | Hire     |     X    | #
            # .......................................................... ................ #
            # CASE 3 | Bookmark |          X           | Send CR  |     X    | Reject   | #
            # ........................................................................... #
            # CASE 4 | Bookmark |          X           |     X    |     X    |     X    | #
            # ........................................................................... #

            # Get length of the recruiter activity list
            length = len(data)
            # get all recruiter events from activity list
            event_list = [recruiter_activity.recruiter_event for recruiter_activity in data]

            # CASE 1: if no activities with a specific talent
            if length <= 0:
                for recruiter_event in recruiter_events:
                    activity = RecruiterActivity()
                    activity.recruiter_event = recruiter_event
                    temp_data.append(activity)
                # print("recruiter activity list is empty")

            # CASE 2: Only Send contact request
            # Bookmark does not exist in the recruiter activity list
            elif recruiter_events[0] not in event_list and length >= 1:
                temp_event_list = event_list
                skipped = True  # checks if some events are skipped
                for recruiter_event in recruiter_events:
                    idx = 0
                    while idx < length:
                        if recruiter_event.id == data[idx].recruiter_event.id:
                            data[idx].is_disabled = True
                            temp_data.append(data[idx])
                            if len(temp_event_list) == 1:
                                skipped = False
                            temp_event_list.remove(recruiter_event)
                            break
                        idx = idx + 1
                    if idx == length:
                        activity = RecruiterActivity()
                        activity.recruiter_event = recruiter_event
                        if skipped:
                            activity.is_disabled = True
                        temp_data.append(activity)
                # print("Only send Contact Request")

            # CASE 3: Bookmark and Send Contact Request
            # Bookmark exists in the recruiter activity list
            elif recruiter_events[0] in event_list and length >= 2:
                temp_event_list = event_list
                skipped = True

                for recruiter_event in recruiter_events:
                    idx = 0
                    while idx < length:
                        if recruiter_event.id == data[idx].recruiter_event.id:
                            data[idx].is_disabled = True
                            temp_data.append(data[idx])
                            # checks if not Bookmark event
                            if len(temp_event_list) == 1:
                                skipped = False
                            temp_event_list.remove(recruiter_event)
                            break
                        idx = idx + 1
                    if idx == length:
                        activity = RecruiterActivity()
                        if skipped:
                            activity.is_disabled = True
                        activity.recruiter_event = recruiter_event
                        temp_data.append(activity)
                # print("Bookmark and CR")

            # CASE 4: Only bookmark
            elif recruiter_events[0] in event_list and length == 1:
                for recruiter_event in recruiter_events:
                    idx = 0
                    while idx < length:
                        if recruiter_event.id == data[idx].recruiter_event.id:
                            if not data[idx].is_updated:
                                data[idx].recruiter_event.name = 'Unbookmark'
                            temp_data.append(data[idx])
                            break
                        idx = idx + 1
                    if idx == length:
                        activity = RecruiterActivity()
                        activity.recruiter_event = recruiter_event
                        temp_data.append(activity)
                # print("Only Bookmark")
        else:
            temp_data = []  # if recruiter does not exist
        return super(FilteredListSerializer, self).to_representation(temp_data)


# The serializer used to list recruiter activities with minimal fields and recruiter event details
class RecruiterActivityWithEventSerializer(serializers.ModelSerializer):

    # Provide details of a specific event
    recruiter_event = RecruiterEventSerializer()

    class Meta:
        list_serializer_class = FilteredListSerializer
        model = RecruiterActivity
        fields = '__all__'


# The serializer used to list recruiter activities with all fields
class RecruiterActivityDetailSerializer(serializers.ModelSerializer):
    recruiter = RecruiterSerializer()
    talent = TalentMiniSerializer()
    recruiter_event = RecruiterEventSerializer()

    class Meta:
        model = RecruiterActivity
        fields = '__all__'


# The serializer used to create a recruiter activity instance
class RecruiterActivityCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecruiterActivity
        read_only_fields = ('event_time', 'is_unchanged')
        fields = '__all__'

    def create(self, validated_data):
        print('Create() method called')
        # create recruiter activity history
        recruiter_activity = RecruiterActivity(
            recruiter=validated_data.get('recruiter', None),
            talent=validated_data.get('talent', None),
            recruiter_event=validated_data.get('recruiter_event', None),
            event_time=timezone.now(),
        )
        recruiter_activity.save()
        # keep history of a specific recruiter
        RecruiterActivityHistoryCreateSerializer.create(
            RecruiterActivityHistoryCreateSerializer(), validated_data=validated_data)

        return recruiter_activity


# The serializer used to update a specific recruiter activity instance
class RecruiterActivityUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecruiterActivity
        read_only_fields = ('event_time',)
        fields = ('recruiter', 'talent', 'recruiter_event', 'event_time', 'is_unchanged')

    def update(self, instance, validated_data):
        with transaction.atomic():
            instance.is_unchanged = validated_data.get('is_unchanged', instance.is_unchanged)
            instance.event_time = timezone.now()
            instance.save()
            print(validated_data)
            # keep history of a specific recruiter
            RecruiterActivityHistoryCreateSerializer.create(
                RecruiterActivityHistoryCreateSerializer(), validated_data=validated_data)

            return instance


# The serializer used to list recruiter activity histories with minimal fields
class RecruiterActivityHistoryMiniSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecruiterActivityHistory
        fields = ('id', 'recruiter', 'talent', 'recruiter_event', 'event_time', 'is_unchanged')


# The serializer used to create a recruiter activity history instance
class RecruiterActivityHistoryCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecruiterActivityHistory
        read_only_fields = ('event_time',)
        fields = ('recruiter', 'talent', 'recruiter_event', 'event_time', 'is_unchanged')

    def create(self, validated_data):
        # create recruiter activity history
        recruiter_activity_history = RecruiterActivityHistory(
            recruiter=validated_data.get('recruiter', None),
            talent=validated_data.get('talent', None),
            recruiter_event=validated_data.get('recruiter_event', None),
            event_time=timezone.now()
        )
        is_unchanged = validated_data.get('is_unchanged', None)
        if is_unchanged is None:
            recruiter_activity_history.is_unchanged = True
        else:
            recruiter_activity_history.is_unchanged = is_unchanged

        recruiter_activity_history.save()
        return recruiter_activity_history
