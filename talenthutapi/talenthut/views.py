from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status

from django.contrib.auth.models import User

from .models import Talent, Address, Expertise, Resume
from .models import JobExperience, TechnicalSkill, Education, LanguageSkill
from .models import Recruiter, RecruiterActivity, RecruiterEvent

from .recruiter_activity_serializers import (RecruiterActivityDetailSerializer, RecruiterActivityMiniSerializer,
                                             RecruiterActivityUpdateSerializer, RecruiterActivityCreateSerializer,
                                             RecruiterActivityHistoryCreateSerializer)
from .resume_serializers import JobExperienceSerializer
from .resume_serializers import TechnicalSkillSerializer, EducationSerializer, LanguageSkillSerializer
from .resume_serializers import ResumeMiniSerializer
from .user_serializers import UserSerializer
from .talent_serializers import (TalentListSerializer, TalentDetailSerializer,
                                 TalentCreateSerializer, TalentUpdateSerializer)
from .recruiter_serializers import RecruiterSerializer, RecruiterCreateSerializer, RecruiterUpdateSerializer
from .other_serializers import RecruiterEventSerializer, ExpertiseSerializer, AddressSerializer


class UserList(APIView):
    """
    List all users or create a user instance
    """
    def get(self, request):
        users = User.objects.all().order_by('first_name', 'last_name')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    """
    Retrieve, update or delete a user instance
    """
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""
------------------- End : Implementation of TALENT model --------------------
"""


"""
------------------- Start : Implementation of TALENT model --------------------
"""


class TalentList(APIView):
    """
    List all talents or create a new talent instance
    """
    def get(self, request):
        talents = Talent.objects.all()
        serializer = TalentListSerializer(talents, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TalentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TalentListByExpertise(APIView):
    """
    List all talents by expertise.
    """

    def get(self, request, expertise_pk):
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


class RecruiterActivityList(APIView):
    """
    List all recruiter activities along with talent information
    """
    def get(self, request, recruiter_pk):

        # distinct is not supported on sqlite3 database
        # recruiter_activities = RecruiterActivity.objects.filter(recruiter=recruiter_pk) \
        # .order_by('talent__user__first_name', 'talent__user__last_name', 'talent__id', '-event_time') \
        #     .distinct('talent__user__first_name', 'talent__user__last_name', 'talent__id')

        # since sqlite3 does not support the distinct property, talents could be duplicated. Fix it later.

        recruiter_activities = RecruiterActivity.objects.filter(recruiter=recruiter_pk) \
            .order_by('talent__user__first_name', 'talent__user__last_name', 'talent__id', '-event_time')
        serializer = RecruiterActivityDetailSerializer(recruiter_activities, many=True)

        return Response(serializer.data)


class RecruiterActivityListByRecruiterEvent(APIView):
    """
    List all recruiter activities by recruiter event along with talent information
    """
    def get(self, request, recruiter_pk, recruiter_event_pk):
        recruiter_activities = RecruiterActivity.objects.filter(recruiter=recruiter_pk, recruiter_event_id=recruiter_event_pk) \
            .order_by('talent__user__first_name', 'talent__user__last_name', 'talent__id')
        serializer = RecruiterActivityDetailSerializer(recruiter_activities, many=True)

        return Response(serializer.data)


class TalentDetail(APIView):
    """
    Retrieve, update or delete a talent instance.
    """
    def get_object(self, pk):
        try:
            return Talent.objects.get(pk=pk)
        except Talent.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        talent = self.get_object(pk)
        serializer = TalentDetailSerializer(talent)
        return Response(serializer.data)

    def put(self, request, pk):
        talent = self.get_object(pk)
        serializer = TalentUpdateSerializer(talent, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        talent = self.get_object(pk)
        talent.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""
------------------- End : Implementation of TALENT model --------------------
"""


"""
------------------- Start : Implementation of HIRE_EVENT model --------------------
"""


# TODO : name has to be adjusted later
class RecruiterActivities(APIView):
    """
    List all recruiters' activities, or create a new recruiter activity
    """
    def get(self, request):
        recruiter_activities = RecruiterActivity.objects.all()
        serializer = RecruiterActivityMiniSerializer(recruiter_activities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RecruiterActivityCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecruiterActivityDetail(APIView):
    """
    Retrieve, update or delete a recruiter activity instance.
    """
    def get_object(self, pk):
        try:
            return RecruiterActivity.objects.get(pk=pk)
        except RecruiterActivity.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        recruiter_activity = self.get_object(pk)
        serializer = RecruiterActivityCreateSerializer(recruiter_activity)
        return Response(serializer.data)

    def put(self, request, pk):
        recruiter_activity = self.get_object(pk)
        serializer = RecruiterActivityUpdateSerializer(recruiter_activity, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
------------------- End : Implementation of HIRE_EVENT model --------------------
"""


"""
------------------- Start : Implementation of HIRE_EVENT_TYPE model --------------------
"""


class RecruiterEventList(APIView):
    """
    List all hire event type, or create a new hire event type.
    """
    def get(self, request):
        recruiter_events = RecruiterEvent.objects.all()
        serializer = RecruiterEventSerializer(recruiter_events, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RecruiterEventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecruiterEventDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return RecruiterEvent.objects.get(pk=pk)
        except RecruiterEvent.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        recruiter_event = self.get_object(pk)
        serializer = RecruiterEventSerializer(recruiter_event)
        return Response(serializer.data)

    def put(self, request, pk):
        recruiter_event = self.get_object(pk)
        serializer = RecruiterEventSerializer(recruiter_event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        recruiter_event = self.get_object(pk)
        recruiter_event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""
------------------- End : Implementation of HIRE_EVENT_TYPE model --------------------
"""


"""
------------------- Start : Implementation of RESUME model --------------------
"""


class ResumeList(APIView):
    """
    List all resumes, or create a new resume instance
    """
    def get(self, request):
        resumes = Resume.objects.all()
        serializer = ResumeMiniSerializer(resumes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ResumeMiniSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResumeDetail(APIView):
    """
    Retrieve, update or delete a resume instance
    """
    def get_object(self, pk):
        try:
            return Resume.objects.get(pk=pk)
        except Resume.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        resume = self.get_object(pk)
        serializer = ResumeMiniSerializer(resume)
        return Response(serializer.data)

    def put(self, request, pk):
        resume = self.get_object(pk)
        serializer = ResumeMiniSerializer(resume, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        resume = self.get_object(pk)
        resume.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""
------------------- End : Implementation of RESUME model --------------------
"""


"""
------------------- Start : Implementation of JOB_EXPERIENCE model --------------------
"""


class JobExperienceList(APIView):
    """
    List all job experiences, or create a new job experience instance
    """
    def get(self, request):
        job_experiences = JobExperience.objects.all()
        serializer = JobExperienceSerializer(job_experiences, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = JobExperienceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobExperienceDetail(APIView):
    """
    Retrieve, update or delete a job experience instance
    """
    def get_object(self, pk):
        try:
            return JobExperience.objects.get(pk=pk)
        except JobExperience.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        job_experience = self.get_object(pk)
        serializer = JobExperienceSerializer(job_experience)
        return Response(serializer.data)

    def put(self, request, pk):
        job_experience = self.get_object(pk)
        serializer = JobExperienceSerializer(job_experience, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        job_experience = self.get_object(pk)
        job_experience.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""
------------------- End : Implementation of JOB_EXPERIENCE model --------------------
"""


"""
------------------- Start : Implementation of TECHNICAL_SKILL model --------------------
"""


class TechnicalSkillList(APIView):
    """
    List all technical skills, or create a new technical skill instance
    """
    def get(self, request):
        technical_skills = TechnicalSkill.objects.all()
        serializer = TechnicalSkillSerializer(technical_skills, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TechnicalSkillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TechnicalSkillDetail(APIView):
    """
    Retrieve, update or delete a technical skill instance
    """
    def get_object(self, pk):
        try:
            return TechnicalSkill.objects.get(pk=pk)
        except TechnicalSkill.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        technical_skill = self.get_object(pk)
        serializer = TechnicalSkillSerializer(technical_skill)
        return Response(serializer.data)

    def put(self, request, pk):
        technical_skill = self.get_object(pk)
        serializer = TechnicalSkillSerializer(technical_skill, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        technical_skill = self.get_object(pk)
        technical_skill.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""
------------------- End : Implementation of TECHNICAL_SKILL model --------------------
"""

"""
------------------- Start : Implementation of EDUCATION model --------------------
"""


class EducationList(APIView):
    """
    List all educations, or create a new education instance
    """
    def get(self, request):
        educations = Education.objects.all()
        serializer = EducationSerializer(educations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EducationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EducationDetail(APIView):
    """
    Retrieve, update or delete an education instance
    """
    def get_object(self, pk):
        try:
            return Education.objects.get(pk=pk)
        except Education.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        education = self.get_object(pk)
        serializer = EducationSerializer(education)
        return Response(serializer.data)

    def put(self, request, pk):
        education = self.get_object(pk)
        serializer = EducationSerializer(education, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        education = self.get_object(pk)
        education.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""
------------------- End : Implementation of EDUCATION model --------------------
"""

"""
------------------- Start : Implementation of LANGUAGE_SKILL model --------------------
"""


class LanguageSkillList(APIView):
    """
    List all language skills, or create a new language skill instance
    """
    def get(self, request):
        language_skills = LanguageSkill.objects.all()
        serializer = LanguageSkillSerializer(language_skills, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LanguageSkillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LanguageSkillDetail(APIView):
    """
    Retrieve, update or delete a language skill instance
    """
    def get_object(self, pk):
        try:
            return LanguageSkill.objects.get(pk=pk)
        except LanguageSkill.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        language_skill = self.get_object(pk)
        serializer = LanguageSkillSerializer(language_skill)
        return Response(serializer.data)

    def put(self, request, pk):
        language_skill = self.get_object(pk)
        serializer = LanguageSkillSerializer(language_skill, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        language_skill = self.get_object(pk)
        language_skill.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""
------------------- End : Implementation of LANGUAGE_SKILL model --------------------
"""

"""
------------------- Start : Implementation of ADDRESS model --------------------
"""


class AddressList(APIView):
    """
    List all addresses, or create a new address instance
    """
    def get(self, request):
        addresses = Address.objects.all()
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressDetail(APIView):
    """
    Retrieve, update or delete an address instance
    """
    def get_object(self, pk):
        try:
            return Address.objects.get(pk=pk)
        except Address.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        address = self.get_object(pk)
        serializer = AddressSerializer(address)
        return Response(serializer.data)

    def put(self, request, pk):
        address = self.get_object(pk)
        serializer = AddressSerializer(address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        address = self.get_object(pk)
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""
------------------- End : Implementation of ADDRESS model --------------------
"""


"""
------------------- Start : Implementation of EXPERTISE model --------------------
"""


class ExpertiseList(APIView):
    """
    List all expertises, or create a new expertise instance
    """
    def get(self, request):
        expertises = Expertise.objects.all()
        serializer = ExpertiseSerializer(expertises, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ExpertiseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpertiseDetail(APIView):
    """
    Retrieve, update or delete an expertise instance
    """
    def get_object(self, pk):
        try:
            return Expertise.objects.get(pk=pk)
        except Expertise.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        expertise = self.get_object(pk)
        serializer = ExpertiseSerializer(expertise)
        return Response(serializer.data)

    def put(self, request, pk):
        expertise = self.get_object(pk)
        serializer = ExpertiseSerializer(expertise, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        expertise = self.get_object(pk)
        expertise.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""
------------------- End : Implementation of EXPERTISE model --------------------
"""


"""
------------------- Start : Implementation of RECRUITER model --------------------
"""


class RecruiterList(APIView):
    """
    List all recruiters, or create a new recruiter instance
    """
    def get(self, request):
        recruiters = Recruiter.objects.all()
        serializer = RecruiterSerializer(recruiters, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RecruiterCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecruiterDetail(APIView):
    """
    Retrieve, update or delete a recruiter instance.
    """
    def get_object(self, pk):
        try:
            return Recruiter.objects.get(pk=pk)
        except Recruiter.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        recruiter = self.get_object(pk)
        serializer = RecruiterSerializer(recruiter)
        return Response(serializer.data)

    def put(self, request, pk):
        recruiter = self.get_object(pk)
        # partial update possible e.g. only username or password can be updated
        serializer = RecruiterUpdateSerializer(recruiter, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        recruiter = self.get_object(pk)
        recruiter.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""
------------------- End : Implementation of RECRUITER model --------------------
"""
