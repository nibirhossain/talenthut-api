from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Talent, Address, Expertise, Resume
from .models import JobExperience, TechnicalSkill, Education, LanguageSkill
from .models import Recruiter, HireEvent, HireEventType


class ExpertiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expertise
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class JobExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobExperience
        fields = '__all__'


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'


class TechnicalSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalSkill
        fields = '__all__'


class LanguageSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = LanguageSkill
        fields = '__all__'


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


class TalentSerializer2(serializers.ModelSerializer):
    # many to many relationship
    expertises = ExpertiseSerializer(many=True, read_only=True)

    # foreign key / one to many relationship

    # one to one relationship

    class Meta:
        model = Talent
        fields = '__all__'


class HireEventSerializer(serializers.ModelSerializer):
    # talent = TalentSerializer2()

    class Meta:
        model = HireEvent
        fields = '__all__'
        # fields = ('talent', '')


class UserSerializer(serializers.ModelSerializer):
    # recruiter = RecruiterSerializer(required=True)

    class Meta:
        model = User
        # fields = '__all__'
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class TalentSerializer(serializers.ModelSerializer):
    # one to one relationship
    user = UserSerializer(required=True)
    # many to many relationship
    expertises = ExpertiseSerializer(many=True, read_only=True)

    # foreign key / one to many relationship
    addresses = AddressSerializer(source='address_set', many=True)

    # one to one relationship
    resume = ResumeSerializer(required=True)

    # foreign key / one to many relationship
    hire_events = HireEventSerializer(source='hireevent_set', many=True)

    class Meta:
        model = Talent
        fields = '__all__'


class RecruiterSerializer(serializers.ModelSerializer):
    hire_events = HireEventSerializer(source='hireevent_set', many=True, required=False)
    user = UserSerializer(required=True)

    class Meta:
        model = Recruiter
        fields = '__all__'


class HireEventTypeSerializer(serializers.ModelSerializer):
    hire_event = HireEventSerializer(source='hireevent_set', many=True, required=False)

    class Meta:
        model = HireEventType
        fields = '__all__'

