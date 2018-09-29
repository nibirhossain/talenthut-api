from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status

from ..models import RecruiterActivity

from ..th_serializers.recruiter_activity import (RecruiterActivityDetailSerializer,
                                                 RecruiterActivityMiniSerializer,
                                                 RecruiterActivityUpdateSerializer,
                                                 RecruiterActivityCreateSerializer,
                                                 RecruiterActivityWithEventSerializer)
from ..th_permissions import IsAdminUserOrRecruiterItself, IsAdminUserOrRecruiter, IsAdminUserOrRecruiterWithPostMethod


class RecruiterActivityList(APIView):

    permission_classes = (IsAdminUserOrRecruiter, )

    def get(self, request, recruiter_pk, *args, **kwargs):

        """
        List all recruiter activities along with talent information
        """

        # TODO: query parameters not found from URL

        # if true, recruiter id will be retrieved from logged in user. Otherwise the user would be admin
        # and the provided 'recruiter_pk' parameter would be used to fetch recruiter activity list
        if request.user and not request.user.is_staff and \
                (getattr(request.user, 'recruiter', False) and recruiter_pk != request.user.recruiter.id):
            data = {"detail": "Unauthorized. You do not have permission to perform this action."}
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

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

    permission_classes = (IsAdminUserOrRecruiter, )

    def get(self, request, recruiter_pk, recruiter_event_pk):
        """
        List all recruiter activities by recruiter event along with talent information
        """

        # if true, recruiter id will be retrieved from logged in user. Otherwise the user would be admin
        # and the provided 'recruiter_pk' parameter would be used to fetch recruiter activity list
        if request.user and not request.user.is_staff and \
                (getattr(request.user, 'recruiter', False) and recruiter_pk != request.user.recruiter.id):
            data = {"detail": "Unauthorized. You do not have permission to perform this action."}
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        recruiter_activities = RecruiterActivity.objects.filter(recruiter=recruiter_pk,
                                                                recruiter_event_id=recruiter_event_pk) \
            .order_by('talent__user__first_name', 'talent__user__last_name', 'talent__id')

        serializer = RecruiterActivityDetailSerializer(recruiter_activities, many=True)

        return Response(serializer.data)


class RecruiterActivitiesByRecruiterAndTalent(APIView):

    permission_classes = (IsAdminUserOrRecruiter, )

    def get(self, request, recruiter_pk, talent_pk):
        """
        List all recruiter activities by recruiter and talent
        """

        # if true, recruiter id will be retrieved from logged in user. Otherwise the user would be admin
        # and the provided 'recruiter_pk' parameter would be used to fetch recruiter activity list
        if request.user and not request.user.is_staff and \
                (getattr(request.user, 'recruiter', False) and recruiter_pk != request.user.recruiter.id):
            data = {"detail": "Unauthorized. You do not have permission to perform this action."}
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        recruiter_activities = RecruiterActivity.objects.filter(recruiter=recruiter_pk, talent=talent_pk) \
            .order_by('talent__user__first_name', 'talent__user__last_name', 'talent__id', '-event_time') \
            # .distinct('talent__user__first_name', 'talent__user__last_name', 'talent__id')
        print(recruiter_activities[0])
        serializer = RecruiterActivityWithEventSerializer(recruiter_activities, many=True, context={'request': request})

        return Response(serializer.data)


# TODO : name has to be adjusted later
class RecruiterActivities(APIView):

    permission_classes = (IsAdminUserOrRecruiterWithPostMethod, )

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
        # check if the provided parameter for recruiter matches with logged in recruiter
        recruiter = request.data.get('recruiter', None)
        if request.user and getattr(request.user, 'recruiter', False) and str(request.user.recruiter.id) != recruiter:
            data = {"detail": "Unauthorized. The provided recruiter argument does not match with logged in recruiter."}
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        serializer = RecruiterActivityCreateSerializer(data=request.data, context={"recruiter": recruiter})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecruiterActivityDetail(APIView):

    permission_classes = (IsAdminUserOrRecruiterItself, )

    def get_object(self):
        obj = get_object_or_404(RecruiterActivity, pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, pk):
        """
        Retrieve a recruiter activity instance.
        """
        recruiter_activity = self.get_object()
        serializer = RecruiterActivityCreateSerializer(recruiter_activity)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update a recruiter activity instance.
        """
        recruiter_activity = self.get_object()
        serializer = RecruiterActivityUpdateSerializer(recruiter_activity, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

