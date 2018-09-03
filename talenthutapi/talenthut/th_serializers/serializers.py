from rest_framework import serializers

from ..models import Address, Expertise, Talent
from ..models import JobExperience, TechnicalSkill, Education, LanguageSkill
from ..models import RecruiterEvent, Sex, MaritalStatus

from .user_serializers import UserSerializer


# The serializer used to list expertises, create, update, delete and detail an expertise
class ExpertiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expertise
        fields = '__all__'


# The serializer used to list addresses, create, update, delete and detail an address
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


# The serializer used to list job experiences, create, update, delete and detail a job experience
class JobExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobExperience
        fields = '__all__'


# The serializer used to list educations, create, update, delete and detail an education
class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'


# The serializer used to list technical skills, create, update, delete and detail a technical skill
class TechnicalSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalSkill
        fields = '__all__'


# The serializer used to list language skills, create, update, delete and detail a language skill
class LanguageSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = LanguageSkill
        fields = '__all__'


# The serializer used to list recruiter events, create, update, delete and detail a recruiter event
class RecruiterEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecruiterEvent
        fields = '__all__'


# The serializer used to list sexes, create, update, delete and detail a sex
class SexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sex
        fields = '__all__'


# The serializer used to list marital statuses, create, update, delete and detail a marital status
class MaritalStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = MaritalStatus
        fields = '__all__'


# The serializer used to list talents with minimal fields
class TalentMiniSerializer(serializers.ModelSerializer):

    # one to one relationship
    user = UserSerializer(required=True)
    # many to many relationship
    expertises = ExpertiseSerializer(many=True, read_only=True)

    class Meta:
        model = Talent
        fields = '__all__'


# The serializer used to list talents with more fields
class TalentDescriptiveSerializer(serializers.ModelSerializer):

    # one to one relationship
    user = UserSerializer(required=True)
    # many to many relationship
    expertises = ExpertiseSerializer(many=True, read_only=True)
    # one to many relationship
    addresses = AddressSerializer(many=True)
    # many to one relationship
    sex = SexSerializer()
    # many to one relationship
    marital_status = MaritalStatusSerializer()

    class Meta:
        model = Talent
        fields = '__all__'
