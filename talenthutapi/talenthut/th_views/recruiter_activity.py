from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status

from ..models import RecruiterActivity

from ..th_serializers.recruiter_activity import (RecruiterActivityDetailSerializer,
                                                 RecruiterActivityMiniSerializer,
                                                 RecruiterActivityUpdateSerializer,
                                                 RecruiterActivityCreateSerializer,
                                                 RecruiterActivityWithEventSerializer)


class RecruiterActivityList(APIView):

    def get(self, request, recruiter_pk):
        """
        List all recruiter activities along with talent information
        """

        # distinct is not supported on sqlite3 database
        # recruiter_activities = RecruiterActivity.objects.filter(recruiter=recruiter_pk) \
        # .order_by('talent__user__first_name', 'talent__user__last_name', 'talent__id', '-event_time') \
        #     .distinct('talent__user__first_name', 'talent__user__last_name', 'talent__id')

        # since sqlite3 does not support the distinct property, talents could be duplicated. Fix it later.

        recruiter_activities = RecruiterActivity.objects.filter(recruiter=recruiter_pk) \
            .order_by('talent__user__first_name', 'talent__user__last_name', 'talent__id', '-event_time') \
            .distinct('talent__user__first_name', 'talent__user__last_name', 'talent__id')
        serializer = RecruiterActivityDetailSerializer(recruiter_activities, many=True)

        return Response(serializer.data)


class RecruiterActivityListByRecruiterEvent(APIView):

    def get(self, request, recruiter_pk, recruiter_event_pk):
        """
        List all recruiter activities by recruiter event along with talent information
        """
        recruiter_activities = RecruiterActivity.objects.filter(recruiter=recruiter_pk, recruiter_event_id=recruiter_event_pk) \
            .order_by('talent__user__first_name', 'talent__user__last_name', 'talent__id')
        serializer = RecruiterActivityDetailSerializer(recruiter_activities, many=True)

        return Response(serializer.data)


class RecruiterActivitiesByRecruiterAndTalent(APIView):
    def get(self, request, recruiter_pk, talent_pk):
        """
        List all recruiter activities by recruiter and talent
        """

        recruiter_activities = RecruiterActivity.objects.filter(recruiter=recruiter_pk, talent=talent_pk) \
            .order_by('talent__user__first_name', 'talent__user__last_name', 'talent__id', '-event_time') \
            # .distinct('talent__user__first_name', 'talent__user__last_name', 'talent__id')
        serializer = RecruiterActivityWithEventSerializer(recruiter_activities, many=True)

        return Response(serializer.data)


# TODO : name has to be adjusted later
class RecruiterActivities(APIView):

    def get(self, request):
        """
        List all recruiters' activities
        """
        recruiter_activities = RecruiterActivity.objects.all()
        serializer = RecruiterActivityMiniSerializer(recruiter_activities, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new recruiter activity
        """
        serializer = RecruiterActivityCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecruiterActivityDetail(APIView):

    def get_object(self, pk):
        try:
            return RecruiterActivity.objects.get(pk=pk)
        except RecruiterActivity.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        Retrieve a recruiter activity instance.
        """
        recruiter_activity = self.get_object(pk)
        serializer = RecruiterActivityCreateSerializer(recruiter_activity)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update a recruiter activity instance.
        """
        recruiter_activity = self.get_object(pk)
        serializer = RecruiterActivityUpdateSerializer(recruiter_activity, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

