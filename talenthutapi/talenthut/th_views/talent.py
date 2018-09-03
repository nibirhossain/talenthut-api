from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from ..models import Talent
from ..th_serializers.talent import (TalentListSerializer, TalentDetailSerializer,
                                     TalentUpdateSerializer, TalentCreateSerializer)


class TalentList(APIView):

    def get(self, request):
        """
        List all talents
        """
        talents = Talent.objects.all()
        serializer = TalentListSerializer(talents, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new talent instance
        """
        serializer = TalentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TalentListByExpertise(APIView):

    def get(self, request, expertise_pk):
        """
        List all talents by expertise.
        """
        # talents = Talent.objects.filter(expertises__id=expertise_pk)
        talents = Talent.objects.filter(expertises=expertise_pk)
        serializer = TalentListSerializer(talents, many=True)
        return Response(serializer.data)


"""
class TalentListByRecruiter(APIView):
    # List all talents by recruiter.

    def get(self, request, recruiter_pk):

        # distinct is not supported on sqlite3 database
        # hire_events = HireEvent.objects.filter(recruiter=recruiter_pk) \
        # .order_by('talent__user__firstname', 'talent__user__lastname', 'talent__id', '-event_time') \
        #     .distinct('talent__fuser__irstname', 'talent__user__lastname', 'talent__id')

        hire_events = HireEvent.objects.filter(recruiter=recruiter_pk)\
        .order_by('talent__user__first_name', 'talent__user__last_name', 'talent__id', '-event_time')

        serializer = HireEventSerializer(hire_events, many=True)
        return Response(serializer.data)
"""


class TalentDetail(APIView):

    def get_object(self, pk):
        try:
            return Talent.objects.get(pk=pk)
        except Talent.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        Retrieve a talent instance.
        """
        talent = self.get_object(pk)
        serializer = TalentDetailSerializer(talent)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update a talent instance.
        """
        talent = self.get_object(pk)
        serializer = TalentUpdateSerializer(talent, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    def delete(self, request, pk):
        talent = self.get_object(pk)
        talent.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    """