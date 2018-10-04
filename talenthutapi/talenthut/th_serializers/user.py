from rest_framework import serializers
from django.db import IntegrityError
from rest_framework.exceptions import APIException
from rest_framework.authtoken.models import Token
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


class CustomValidation(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'

    def __init__(self, detail, field, status_code):
        if status_code is not None:
            self.status_code = status_code
        if detail is not None:
            # self.detail = {field: force_text(detail)}
            self.detail = {"user": {field: [force_text(detail)]}}
        else:
            self.detail = {'detail': force_text(self.default_detail)}


# This custom validator handles user related exceptions
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
        # fields = ('id', 'username', 'first_name', 'last_name', 'email')
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            }


# The serializer used to create a user instance
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
                # create user
                user = User(
                    email=email,
                    username=username,
                    first_name=first_name,
                    last_name=last_name
                )
                user.set_password(validated_data['password'])
                user.save()
                Token.objects.create(user=user)
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
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'username': {'validators': []},
            'first_name': {'required': False},
            'last_name': {'required': False}
        }

    def update(self, instance, validated_data):
        username = validated_data.get('username', None)

        with transaction.atomic():
            try:
                instance.username = validated_data.get('username', instance.username)
                instance.email = validated_data.get('email', instance.email)
                instance.first_name = validated_data.get('first_name', instance.first_name)
                instance.last_name = validated_data.get('last_name', instance.last_name)
                password = validated_data.get('password', None)

                if password is not None:
                    instance.set_password(password)
                    print("Password has been successfully changed.")
                instance.save()

                return instance
            except IntegrityError:
                # create a dictionary and send all fields to check for which one gets exception
                field_dict = {'username': username}
                print(field_dict)
                # handle user related exceptions
                raise CustomValidation('Username already exists', 'username', status_code=status.HTTP_409_CONFLICT)




