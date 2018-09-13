from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from ..models import Talent, Recruiter
from ..th_serializers.talent import TalentSerializer
from ..th_serializers.recruiter import RecruiterSerializer
from ..th_serializers.user import UserSerializer


class HomeView(APIView):

    permission_classes = (AllowAny, )

    def get(self, request):
        return Response('Home Page of TalentHut REST APIs. Version 1.0.0')


class LoginView(APIView):

    permission_classes = (AllowAny, )

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

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
