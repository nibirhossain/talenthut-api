from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from ..models import Talent, Recruiter
from ..th_serializers.talent import TalentSerializer, TalentCreateSerializer
from ..th_serializers.recruiter import RecruiterSerializer, RecruiterCreateSerializer
from ..th_serializers.user import UserSerializer


class HomeView(APIView):

    permission_classes = (AllowAny, )

    def get(self, request):
        return Response('Home Page of TalentHut REST APIs. Version 1.0.0')


class LoginView(APIView):

    permission_classes = (AllowAny, )

    def post(self, request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        user = authenticate(username=username, password=password)

        if user and user.is_active and user.is_staff:
            token, created = Token.objects.get_or_create(user=user)
            serializer = UserSerializer(user)
            return Response({'token': token.key, 'admin': serializer.data})

        elif user and user.is_active:
            try:
                recruiter = Recruiter.objects.get(user=user)
                serializer = RecruiterSerializer(recruiter)
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key, 'recruiter': serializer.data})
            except ObjectDoesNotExist:
                try:
                    talent = Talent.objects.get(user=user)
                    serializer = TalentSerializer(talent)
                    token, _ = Token.objects.get_or_create(user=user)
                    return Response({'token': token.key, 'talent': serializer.data})
                except ObjectDoesNotExist:
                    return Response({"Exception": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class SignupRecruiterView(APIView):

    permission_classes = (AllowAny, )

    def post(self, request):
        """
        Create a new recruiter instance.
        """
        user = request.data.get('user', None)
        if user:
            email = user.get('email', None)
            print(user)
            password = user.get('password', None)
            password_confirmation = user.get('password_confirmation', None)
            # set username to email
            user['username'] = email
        company_name = request.data.get('company_name', None)

        if not email or not password or not company_name:
            error = {'error': 'username or password or company name could not be empty'}
            return Response(data=error, status=status.HTTP_400_BAD_REQUEST)
        elif password != password_confirmation:
            error = {'error': 'password did not match'}
            return Response(data=error, status=status.HTTP_400_BAD_REQUEST)

        serializer = RecruiterCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignupTalentView(APIView):

    permission_classes = (AllowAny, )

    def post(self, request):
        """
        Create a new talent instance
        """
        user = request.data.get('user', None)
        if user:
            email = user.get('email', None)
            password = user.get('password', None)
            password_confirmation = user.get('password_confirmation', None)
            # set username to email
            user['username'] = email

        if not email or not password:
            error = {'error': 'username or password could not be empty'}
            return Response(data=error, status=status.HTTP_400_BAD_REQUEST)
        elif password != password_confirmation:
            error = {'error': 'password did not match'}
            return Response(data=error, status=status.HTTP_400_BAD_REQUEST)

        serializer = TalentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
