from rest_framework import serializers

from .models import Resume
from .other_serializers import (JobExperienceSerializer, TechnicalSkillSerializer,
                                LanguageSkillSerializer, EducationSerializer)


# The serializer is used in other serializers and in views
class ResumeMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = '__all__'


# The serializer is used in other serializers and in views
class ResumeDetailSerializer(serializers.ModelSerializer):
    # foreign key / one to many relationship
    job_experiences = JobExperienceSerializer(many=True, required=False)
    # foreign key / one to many relationship
    technical_skills = TechnicalSkillSerializer(many=True, required=False)
    # foreign key / one to many relationship
    language_skills = LanguageSkillSerializer(many=True, required=False)
    # foreign key / one to many relationship
    educations = EducationSerializer(many=True, required=False)

    class Meta:
        model = Resume
        fields = '__all__'
