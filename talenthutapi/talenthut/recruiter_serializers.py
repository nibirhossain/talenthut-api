from rest_framework import serializers

from .models import Recruiter

from .user_serializers import UserSerializer


class RecruiterSerializer(serializers.ModelSerializer):
    # hire_events = HireEventSerializer(source='hireevent_set', many=True, required=False)
    user = UserSerializer(required=True)

    class Meta:
        model = Recruiter
        fields = '__all__'

