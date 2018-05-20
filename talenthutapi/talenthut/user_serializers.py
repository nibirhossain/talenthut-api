from rest_framework import serializers
from django.db import IntegrityError
from rest_framework.exceptions import APIException
from django.utils.encoding import force_text
from rest_framework import status
from django.contrib.auth.models import User
from django.db import transaction


"""
class UserCustomValidation(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'A server error occurred.'

    def __init__(self, detail, field, status_code):
        if status_code is not None:self.status_code = status_code
        if detail is not None:
            self.detail = {field: force_text(detail)}
            # self.detail = {"name": [{"message": "This field is required.", "code": "required"}]}
        else:
            self.detail = {'detail': force_text(self.default_detail)}
"""


# handle user related exceptions
class UserCustomValidation(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'A server error occurred.'

    def __init__(self, field_dict):
        if field_dict is not None:
            for key, value in field_dict.items():
                if not value:
                    # self.detail = {key: force_text(key + ' could not be empty')}
                    self.detail = {"user": {key: [force_text(key + ' could not be empty')]}}
                    break
        else:
            self.detail = {'detail': force_text(self.default_detail)}


# The serializer used to list users and to detail a specific user
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


# The serializer used to create user
class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        email = validated_data.get('email', None)
        username = validated_data.get('username', None)
        first_name = validated_data.get('first_name', None)
        last_name = validated_data.get('last_name', None)

        with transaction.atomic():
            try:
                # create use
                user = User(
                    email=email,
                    username=username,
                    first_name=first_name,
                    last_name=last_name
                )
                user.set_password(validated_data['password'])
                user.save()

                return user
            except IntegrityError:
                # create a dictionary and send all fields to check for which one gets exception
                field_dict = {'username': username, 'first_name': first_name, 'last_name': last_name, 'email': email}
                # handle user related exceptions
                raise UserCustomValidation(field_dict)


# The serializer used to update a specific user
class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        with transaction.atomic():
            try:
                instance.username = validated_data.get('username', instance.username)
                instance.email = validated_data.get('email', instance.email)
                instance.first_name = validated_data.get('first_name', instance.first_name)
                instance.last_name = validated_data.get('last_name', instance.last_name)
                password = validated_data.get('password', None)

                if password is None:
                    instance.set_password(password)
                    print("Password has been successfully changed.")
                instance.save()

                return instance
            except IntegrityError:
                # create a dictionary and send all fields to check for which one gets exception
                field_dict = {'first_name': instance.first_name, 'last_name': instance.last_name, 'email': instance.email}
                # handle user related exception
                raise UserCustomValidation(field_dict)

