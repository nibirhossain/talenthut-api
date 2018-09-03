from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from ..models import Education
from ..th_serializers.resume import EducationSerializer


class EducationList(APIView):

    def get(self, request):
        """
        List all educations.
        """
        educations = Education.objects.all()
        serializer = EducationSerializer(educations, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new education instance.
        """
        serializer = EducationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EducationDetail(APIView):

    def get_object(self, pk):
        try:
            return Education.objects.get(pk=pk)
        except Education.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        Retrieve an education instance.
        """
        education = self.get_object(pk)
        serializer = EducationSerializer(education)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update an education instance
        """
        education = self.get_object(pk)
        serializer = EducationSerializer(education, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    def delete(self, request, pk):
        education = self.get_object(pk)
        education.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    """