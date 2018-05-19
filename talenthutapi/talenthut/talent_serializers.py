from rest_framework import serializers
from django.db import transaction

from .models import Talent
from .user_serializers import UserSerializer
from .resume_serializers import (SexSerializer, ExpertiseSerializer,
                               AddressSerializer, MaritalStatusSerializer, HireEventSerializer,
                               ResumeSerializer)


# The serializer is used in views
class TalentListSerializer(serializers.ModelSerializer):
    # one to one relationship
    user = UserSerializer(required=True)
    # many to many relationship
    expertises = ExpertiseSerializer(many=True, read_only=True)
    # one to many relationship
    addresses = AddressSerializer(source='address_set', many=True)
    # many to one relationship
    sex = SexSerializer()
    # many to one relationship
    marital_status = MaritalStatusSerializer()
    # one to many relationship
    hire_events = HireEventSerializer(source='hireevent_set', many=True)

    class Meta:
        model = Talent
        fields = '__all__'


# The serializer is used in views
class TalentDetailSerializer(serializers.ModelSerializer):
    # one to one relationship
    user = UserSerializer(required=True)
    # many to many relationship
    expertises = ExpertiseSerializer(many=True, read_only=True)
    # one to many relationship
    addresses = AddressSerializer(source='address_set', many=True)
    # many to one relationship
    sex = SexSerializer()
    # many to one relationship
    marital_status = MaritalStatusSerializer()
    # one to many relationship
    hire_events = HireEventSerializer(source='hireevent_set', many=True)
    # one to one relationship
    resume = ResumeSerializer()

    class Meta:
        model = Talent
        fields = '__all__'


# The serializer is used in other serializers
class TalentSerializer(serializers.ModelSerializer):
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

    def update(self, instance, validated_data):
        with transaction.atomic():
            user_data = validated_data.pop('user')
            UserSerializer.update(UserSerializer(), instance.user, validated_data=user_data)

            expertise_data = validated_data.pop('expertises')

            # Remove all existing expertises from the current talent
            for expertise in instance.expertises.all():
                instance.expertises.remove(expertise)

            # Add new expertises to the current talent
            for expertise in expertise_data:
                instance.expertises.add(expertise)

            instance.save()

            return instance

