from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from ..models import Expertise
from ..th_serializers.serializers import ExpertiseSerializer


class ExpertiseList(APIView):

    def get(self, request):
        """
        List all expertises.
        """
        expertises = Expertise.objects.all()
        serializer = ExpertiseSerializer(expertises, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new expertise instance.
        """
        serializer = ExpertiseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpertiseDetail(APIView):

    def get_object(self, pk):
        try:
            return Expertise.objects.get(pk=pk)
        except Expertise.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        Retrieve an expertise instance.
        """
        expertise = self.get_object(pk)
        serializer = ExpertiseSerializer(expertise)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update an expertise instance.
        """
        expertise = self.get_object(pk)
        serializer = ExpertiseSerializer(expertise, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    def delete(self, request, pk):
        expertise = self.get_object(pk)
        expertise.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    """
