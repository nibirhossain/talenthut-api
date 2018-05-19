from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Talent, Address, Expertise, Resume
from .models import JobExperience, TechnicalSkill, Education, LanguageSkill
from .models import Recruiter, HireEvent, HireEventType, Sex, MaritalStatus

from django.db import transaction


# The serializer is used in other serializers and in views
class ExpertiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expertise
        fields = '__all__'


# The serializer is used in other serializers and in views
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


# The serializer is used in other serializers and in views
class JobExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobExperience
        fields = '__all__'


# The serializer is used in other serializers and in views
class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'


# The serializer is used in other serializers and in views
class TechnicalSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalSkill
        fields = '__all__'


# The serializer is used in other serializers and in views
class LanguageSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = LanguageSkill
        fields = '__all__'


# The serializer is used in other serializers and in views
class ResumeSerializer(serializers.ModelSerializer):
    # foreign key / one to many relationship
    job_experiences = JobExperienceSerializer(source='jobexperience_set', many=True, required=False)
    # foreign key / one to many relationship
    technical_skills = TechnicalSkillSerializer(source='technicalskill_set', many=True, required=False)
    # foreign key / one to many relationship
    language_skills = LanguageSkillSerializer(source='languageskill_set', many=True, required=False)
    # foreign key / one to many relationship
    educations = EducationSerializer(source='education_set', many=True, required=False)

    class Meta:
        model = Resume
        fields = '__all__'


# The serializer is used in other serializers and in views
class HireEventTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = HireEventType
        fields = '__all__'


# The serializer is used in other serializers
class HireEventSerializer(serializers.ModelSerializer):
    hire_event_type = HireEventTypeSerializer()

    class Meta:
        model = HireEvent
        fields = '__all__'
        # fields = ('talent', '')


# The serializer is used in views
class HireEventListAndDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = HireEvent
        fields = '__all__'
        # fields = ('talent', '')


# The serializer is used in views
class UserPasswordUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('password',)
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        if validated_data['password'] is not None:
            instance.set_password(validated_data['password'])
            instance.save()
        else:
            print('Password could not be empty')

        return instance


# The serializer is used in views
class UserNameUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username',)

    def update(self, instance, validated_data):
        if validated_data['username'] is not None:
            instance.username = validated_data.get('username', instance.username)
            instance.save()
        else:
            print('Username could not be empty')

        return instance


# The serializer is used in views
class UserCreateSerializer(serializers.ModelSerializer):
    # recruiter = RecruiterSerializer(required=True)

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


# The serializer is used in other serializers and in views
class UserUpdateSerializer(serializers.ModelSerializer):
    # recruiter = RecruiterSerializer(required=True)

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()

        return instance


# The serializer is used in other serializers and in views
class UserSerializer(serializers.ModelSerializer):
    # recruiter = RecruiterSerializer(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


# The serializer is used in other serializers and in views
class SexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sex
        fields = '__all__'


# The serializer is used in other serializers and in views
class MaritalStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = MaritalStatus
        fields = '__all__'


class RecruiterSerializer(serializers.ModelSerializer):
    # hire_events = HireEventSerializer(source='hireevent_set', many=True, required=False)
    user = UserSerializer(required=True)

    class Meta:
        model = Recruiter
        fields = '__all__'

