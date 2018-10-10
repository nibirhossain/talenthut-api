from rest_framework import serializers
from django.db import transaction

from ..models import Talent
from .user import UserSerializer, UserUpdateSerializer, UserCreateSerializer
from .recruiter_activity import RecruiterActivityWithEventSerializer
from .resume import ResumeDetailSerializer
from .serializers import TalentDescriptiveSerializer, ExpertiseSerializer


# The serializer used to list talents with minimal fields
class TalentMiniSerializer(serializers.ModelSerializer):

    # one to one relationship
    user = UserSerializer(required=True)
    # many to many relationship
    expertises = ExpertiseSerializer(many=True, read_only=True)

    class Meta:
        model = Talent
        fields = '__all__'


class TalentSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Talent
        fields = ('id', 'user')


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
            # create user
            user_data = validated_data.pop('user', None)
            # user = User.objects.create(**user_data)
            user = UserCreateSerializer.create(UserCreateSerializer(), validated_data=user_data)
            # create talent
            talent = Talent.objects.create(user=user, **validated_data)

            return talent


# The serializer used to update a specific talent instance
class TalentUpdateSerializer(serializers.ModelSerializer):
    # one to one relationship
    user = UserUpdateSerializer(required=True)

    class Meta:
        model = Talent
        # fields = '__all__'
        fields = ('id', 'user', 'experience', 'birthdate', 'mobile', 'qualification', 'birthplace', 'photo',
                  'description', 'sex', 'marital_status', 'expertises')

    def update(self, instance, validated_data):
        with transaction.atomic():
            # update user portion
            user_data = validated_data.pop('user', None)
            UserUpdateSerializer.update(UserUpdateSerializer(), instance.user, validated_data=user_data)

            # update talent portion
            instance.experience = validated_data.get('experience', instance.experience)
            instance.birthdate = validated_data.get('birthdate', instance.birthdate)
            instance.mobile = validated_data.get('mobile', instance.mobile)
            instance.qualification = validated_data.get('qualification', instance.qualification)
            instance.birthplace = validated_data.get('birthplace', instance.birthplace)
            instance.photo = validated_data.get('photo', instance.photo)
            instance.description = validated_data.get('description', instance.description)
            instance.sex = validated_data.get('sex', instance.sex)
            instance.marital_status = validated_data.get('marital_status', instance.marital_status)

            # talent's expertise
            expertise_data = validated_data.pop('expertises', None)
            if expertise_data is not None:
                # Remove all existing expertises from the current talent
                for expertise in instance.expertises.all():
                    instance.expertises.remove(expertise)

                # Add new expertises to the current talent
                for expertise in expertise_data:
                    instance.expertises.add(expertise)
            instance.save()

            return instance

