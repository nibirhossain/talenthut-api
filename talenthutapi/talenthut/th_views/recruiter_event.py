from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from ..models import RecruiterEvent
from ..th_serializers.serializers import RecruiterEventSerializer


class RecruiterEventList(APIView):

    def get(self, request):
        """
        List all recruiter events.
        """
        recruiter_events = RecruiterEvent.objects.all()
        serializer = RecruiterEventSerializer(recruiter_events, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new recruiter event.
        """
        serializer = RecruiterEventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecruiterEventDetail(APIView):

    def get_object(self, pk):
        try:
            return RecruiterEvent.objects.get(pk=pk)
        except RecruiterEvent.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        Retrieve recruiter event instance.
        """
        recruiter_event = self.get_object(pk)
        serializer = RecruiterEventSerializer(recruiter_event)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update a recruiter event instance.
        """
        recruiter_event = self.get_object(pk)
        serializer = RecruiterEventSerializer(recruiter_event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    def delete(self, request, pk):
        recruiter_event = self.get_object(pk)
        recruiter_event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    """

"""
------------------- End : Implementation of HIRE_EVENT_TYPE model --------------------
"""
