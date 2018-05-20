from rest_framework import serializers

from .models import Address, Expertise, Resume

from .models import JobExperience, TechnicalSkill, Education, LanguageSkill
from .models import HireEventType, Sex, MaritalStatus


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

