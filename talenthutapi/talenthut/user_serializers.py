from rest_framework import serializers
from django.contrib.auth.models import User


# The serializer is used in views
class UserPasswordUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('password',)
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        if validated_data['password'] is not None:
            instance.set_password(validated_data['password'])
            instance.save()
        else:
            print('Password could not be empty')

        return instance


# The serializer is used in views
class UserNameUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username',)

    def update(self, instance, validated_data):
        if validated_data['username'] is not None:
            instance.username = validated_data.get('username', instance.username)
            instance.save()
        else:
            print('Username could not be empty')

        return instance


# The serializer is used in views
class UserCreateSerializer(serializers.ModelSerializer):
    # recruiter = RecruiterSerializer(required=True)

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


# The serializer is used in other serializers and in views
class UserUpdateSerializer(serializers.ModelSerializer):
    # recruiter = RecruiterSerializer(required=True)

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()

        return instance


# The serializer is used in other serializers and in views
class UserSerializer(serializers.ModelSerializer):
    # recruiter = RecruiterSerializer(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')
