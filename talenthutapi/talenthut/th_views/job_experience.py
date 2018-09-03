from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from ..models import JobExperience
from ..th_serializers.resume import JobExperienceSerializer


class JobExperienceList(APIView):

    def get(self, request):
        """
        List all job experiences.
        """
        job_experiences = JobExperience.objects.all()
        serializer = JobExperienceSerializer(job_experiences, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new job experience instance.
        """
        serializer = JobExperienceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobExperienceDetail(APIView):

    def get_object(self, pk):
        try:
            return JobExperience.objects.get(pk=pk)
        except JobExperience.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        Retrieve a job experience instance.
        """
        job_experience = self.get_object(pk)
        serializer = JobExperienceSerializer(job_experience)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update a job experience instance
        """
        job_experience = self.get_object(pk)
        serializer = JobExperienceSerializer(job_experience, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    def delete(self, request, pk):
        job_experience = self.get_object(pk)
        job_experience.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    """
