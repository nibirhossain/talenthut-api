from rest_framework import serializers
from django.db import transaction

from .models import Talent
from .user_serializers import UserSerializer
from .recruiter_activity_serializers import RecruiterActivityWithEventSerializer
from .resume_serializers import ResumeDetailSerializer
from .other_serializers import TalentDescriptiveSerializer


# The serializer used to list talents
class TalentListSerializer(TalentDescriptiveSerializer):

    class Meta:
        model = Talent
        fields = '__all__'


# The serializer used to list talent with all fields
class TalentDetailSerializer(TalentDescriptiveSerializer):

    # one to many relationship
    recruiter_activities = RecruiterActivityWithEventSerializer(many=True)
    # one to one relationship
    resume = ResumeDetailSerializer()

    class Meta:
        model = Talent
        fields = '__all__'


# The serializer used to create a talent instance
class TalentCreateSerializer(serializers.ModelSerializer):
    # one to one relationship
    user = UserSerializer(required=True)

    class Meta:
        model = Talent
        fields = '__all__'

    def create(self, validated_data):
        with transaction.atomic():
            user_data = validated_data.pop('user')
            user = UserSerializer.create(UserSerializer(), validated_data=user_data)
            print(user)
            expertise_data = validated_data.pop('expertises')
            talent = Talent.objects.create(user=user, **validated_data)
            # use set() method to insert/update many-to-many relationship all at once
            # in case of add() method, use for loop to insert/update
            # Direct assignment not possible in many-to-many relationship

            # talent.expertises.set(expertise_data)
            for expertise in expertise_data:
                talent.expertises.add(expertise)

            return talent


# The serializer used to update a specific talent instance
class TalentUpdateSerializer(serializers.ModelSerializer):
    # one to one relationship
    user = UserSerializer(required=True)

    class Meta:
        model = Talent
        fields = '__all__'

    def update(self, instance, validated_data):
        with transaction.atomic():
            user_data = validated_data.pop('user')
            UserSerializer.update(UserSerializer(), instance.user, validated_data=user_data)

            expertise_data = validated_data.pop('expertises')

            if expertise_data is not None:
                # Remove all existing expertises from the current talent
                for expertise in instance.expertises.all():
                    instance.expertises.remove(expertise)

                # Add new expertises to the current talent
                for expertise in expertise_data:
                    instance.expertises.add(expertise)
            instance.save()

            return instance

