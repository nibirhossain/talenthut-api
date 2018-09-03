from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from ..models import Recruiter
from ..th_serializers.recruiter import (RecruiterSerializer, RecruiterCreateSerializer,
                                        RecruiterUpdateSerializer)


class RecruiterList(APIView):

    def get(self, request):
        """
        List all recruiters.
        """
        recruiters = Recruiter.objects.all()
        serializer = RecruiterSerializer(recruiters, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new recruiter instance.
        """
        serializer = RecruiterCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecruiterDetail(APIView):

    def get_object(self, pk):
        try:
            return Recruiter.objects.get(pk=pk)
        except Recruiter.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        Retrieve a recruiter instance.
        """
        recruiter = self.get_object(pk)
        serializer = RecruiterSerializer(recruiter)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update a recruiter instance.
        """
        recruiter = self.get_object(pk)
        # partial update possible e.g. only username or password can be updated
        serializer = RecruiterUpdateSerializer(recruiter, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    def delete(self, request, pk):
        recruiter = self.get_object(pk)
        recruiter.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    """
