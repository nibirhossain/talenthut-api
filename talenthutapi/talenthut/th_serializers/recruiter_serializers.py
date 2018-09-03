from rest_framework import serializers
from django.db import transaction
from django.db import IntegrityError
from rest_framework.exceptions import APIException
from django.utils.encoding import force_text
from rest_framework import status

from ..models import Recruiter
from .user_serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer


# The custom validator handles recruiter related exceptions
class RecruiterCustomValidation(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'A server error occurred.'

    def __init__(self, field_dict):
        if field_dict is not None:
            for key, value in field_dict.items():
                if not value:
                    # self.detail = {key: force_text(key + ' could not be empty')}
                    self.detail = {"recruiter": {key: [force_text(key + ' could not be empty')]}}
                    break
        else:
            self.detail = {'detail': force_text(self.default_detail)}


# The serializer used to list recruiters and to detail a specific recruiter
class RecruiterSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Recruiter
        fields = ('id', 'user', 'company_name', 'company_website', 'position')


# The serializer used to create recruiter
class RecruiterCreateSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer(required=True)

    class Meta:
        model = Recruiter
        # fields = '__all__'
        fields = ('user', 'company_name', 'company_website', 'position')

    def create(self, validated_data):
        company_name = validated_data.get('company_name', None)
        position = validated_data.get('position', None)

        with transaction.atomic():
            try:
                user_data = validated_data.pop('user')
                user = UserCreateSerializer.create(UserCreateSerializer(), validated_data=user_data)
                if user is not None:
                    recruiter = Recruiter.objects.create(user=user, **validated_data)
                else:
                    print('Recruiter is not created.')
                return recruiter
            except IntegrityError:
                # create a dictionary and send all fields to check for which one gets exception
                field_dict = {'company_name': company_name, 'position': position}
                # handle recruiter related exceptions
                raise RecruiterCustomValidation(field_dict)


# The serializer used to update a specific recruiter
class RecruiterUpdateSerializer(serializers.ModelSerializer):
    user = UserUpdateSerializer(required=True)

    class Meta:
        model = Recruiter
        fields = ('user', 'company_name', 'company_website', 'position')

    def update(self, instance, validated_data):
        with transaction.atomic():
            user_data = validated_data.pop('user')
            UserUpdateSerializer.update(UserUpdateSerializer(), instance.user, validated_data=user_data)
            instance.company_name = validated_data.get('company_name', instance.company_name)
            instance.company_website = validated_data.get('company_website', instance.company_website)
            instance.position = validated_data.get('position', instance.position)
            instance.save()

            return instance

