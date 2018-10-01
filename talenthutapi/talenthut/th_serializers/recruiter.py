from rest_framework import serializers
from django.db import transaction
from django.contrib.auth.models import User
from rest_framework.exceptions import APIException
from django.utils.encoding import force_text
from rest_framework import status

from ..models import Recruiter
from .user import UserSerializer, UserUpdateSerializer


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

    user = UserSerializer(required=True)

    class Meta:
        model = Recruiter
        # fields = '__all__'
        fields = ('id', 'user', 'company_name', 'company_website', 'position')

    def create(self, validated_data):
        with transaction.atomic():
            user_data = validated_data.pop('user')
            # create user
            user = User.objects.create(**user_data)
            # create recruiter
            recruiter = Recruiter.objects.create(user=user, **validated_data)

            return recruiter


# The serializer used to update a specific recruiter
class RecruiterUpdateSerializer(serializers.ModelSerializer):
    user = UserUpdateSerializer(required=True)

    class Meta:
        model = Recruiter
        fields = ('id', 'user', 'company_name', 'company_website', 'position')

    def update(self, instance, validated_data):
        with transaction.atomic():
            # update user portion
            user_data = validated_data.pop('user', None)
            UserUpdateSerializer.update(UserUpdateSerializer(), instance.user, validated_data=user_data)

            # update recruiter portion
            instance.company_name = validated_data.get('company_name', instance.company_name)
            instance.company_website = validated_data.get('company_website', instance.company_website)
            instance.position = validated_data.get('position', instance.position)
            instance.save()

            return instance


