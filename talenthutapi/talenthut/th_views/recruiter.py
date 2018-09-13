from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from ..models import Recruiter
from ..th_serializers.recruiter import (RecruiterSerializer, RecruiterCreateSerializer,
                                        RecruiterUpdateSerializer)
from ..th_permissions import IsAdminUserOrRecruiterItself


class RecruiterList(APIView):

    permission_classes = (IsAdminUser, )

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

    permission_classes = (IsAdminUserOrRecruiterItself, )

    def get_object(self):
        obj = get_object_or_404(Recruiter, pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, pk):
        """
        Retrieve a recruiter instance.
        """
        recruiter = self.get_object()
        serializer = RecruiterSerializer(recruiter)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update a recruiter instance.
        """
        recruiter = self.get_object()
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
