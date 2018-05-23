from rest_framework import serializers

from .models import RecruiterActivity
from .other_serializers import RecruiterEventSerializer
from .recruiter_serializers import RecruiterSerializer
from .other_serializers import TalentMiniSerializer


# The serializer is used in other serializers
class RecruiterActivityMiniSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecruiterActivity
        fields = '__all__'


# The serializer is used in other serializers
class RecruiterActivityWithEventSerializer(serializers.ModelSerializer):
    recruiter_event = RecruiterEventSerializer()

    class Meta:
        model = RecruiterActivity
        fields = '__all__'


# The serializer is used in other serializers
class RecruiterActivityDetailSerializer(serializers.ModelSerializer):
    recruiter = RecruiterSerializer()
    talent = TalentMiniSerializer()
    recruiter_event = RecruiterEventSerializer()

    class Meta:
        model = RecruiterActivity
        fields = '__all__'


# The serializer is used in other serializers
class RecruiterActivityCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecruiterActivity
        read_only_fields = ('event_time',)
        fields = '__all__'

