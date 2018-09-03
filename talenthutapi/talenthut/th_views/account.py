from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from ..models import Talent, Recruiter
from ..th_serializers.talent import TalentSerializer
from ..th_serializers.recruiter import RecruiterSerializer


class HomeView(APIView):

    def get(self, request):
        return Response('Home Page of TalentHut REST APIs. Version 1.0.0')


class LoginView(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        # TODO: review the below authentication section
        if user and user.is_active:
            try:
                recruiter = Recruiter.objects.get(user=user)
                serializer = RecruiterSerializer(recruiter)
                return Response(serializer.data)
            except ObjectDoesNotExist:
                try:
                    talent = Talent.objects.get(user=user)
                    serializer = TalentSerializer(talent)
                    return Response(serializer.data)
                except ObjectDoesNotExist:
                    return Response({"Exception": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)
