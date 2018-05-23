from rest_framework import serializers

from .models import Address, Expertise, Talent
from .models import JobExperience, TechnicalSkill, Education, LanguageSkill
from .models import RecruiterEvent, Sex, MaritalStatus

from .user_serializers import UserSerializer


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
class RecruiterEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecruiterEvent
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


# The serializer is used in views
class TalentMiniSerializer(serializers.ModelSerializer):

    # one to one relationship
    user = UserSerializer(required=True)
    # many to many relationship
    expertises = ExpertiseSerializer(many=True, read_only=True)

    class Meta:
        model = Talent
        fields = '__all__'


# The serializer is used in views
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
