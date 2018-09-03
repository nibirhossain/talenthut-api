from rest_framework import serializers

from django.db import transaction
from django.utils import timezone

from ..models import RecruiterActivity, RecruiterActivityHistory
from .serializers import RecruiterEventSerializer
from .recruiter_serializers import RecruiterSerializer
from .serializers import TalentMiniSerializer


# The serializer used to list recruiter activities with minimal fields
class RecruiterActivityMiniSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecruiterActivity
        fields = '__all__'


# The serializer used to list recruiter activities with minimal fields and recruiter event details
class RecruiterActivityWithEventSerializer(serializers.ModelSerializer):
    recruiter_event = RecruiterEventSerializer()

    class Meta:
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


"""
--------------------------------------------------------------------------------------------------
"""


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
