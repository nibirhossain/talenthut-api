from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from django.contrib.auth import authenticate
from rest_framework import status

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from .models import Talent, Address, Expertise, Resume
from .models import JobExperience, TechnicalSkill, Education, LanguageSkill
from .models import Recruiter, RecruiterActivity, RecruiterEvent

from .recruiter_activity_serializers import (RecruiterActivityDetailSerializer, RecruiterActivityMiniSerializer,
                                             RecruiterActivityUpdateSerializer, RecruiterActivityCreateSerializer)
from .resume_serializers import JobExperienceSerializer
from .resume_serializers import TechnicalSkillSerializer, EducationSerializer, LanguageSkillSerializer
from .resume_serializers import ResumeMiniSerializer
from .user_serializers import UserSerializer
from .talent_serializers import (TalentListSerializer, TalentDetailSerializer,
                                 TalentCreateSerializer, TalentUpdateSerializer, TalentSerializer)
from .recruiter_serializers import RecruiterSerializer, RecruiterCreateSerializer, RecruiterUpdateSerializer
from .other_serializers import RecruiterEventSerializer, ExpertiseSerializer, AddressSerializer


class HomeView(APIView):

    def get(self, request):
        return Response('Home Page of TalentHut REST APIs. Version 1.0.0')


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        # TODO: review the below authentication section
        if user and user.is_active:
            try:
                recruiter = Recruiter.objects.get(user=user)
                serializer = RecruiterSerializer(recruiter)
                return Response(serializer.data)
            except ObjectDoesNotExist:
                try:
                    talent = Talent.objects.get(user=user)
                    serializer = TalentSerializer(talent)
                    return Response(serializer.data)
                except ObjectDoesNotExist:
                    return Response({"Exception": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class UserList(APIView):

    def get(self, request):
        """
        List all users
        """
        users = User.objects.all().order_by('first_name', 'last_name')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a user instance
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        Retrieve a user instance
        """
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update a user instance
        """
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    """


"""
------------------- End : Implementation of TALENT model --------------------
"""


"""
------------------- Start : Implementation of TALENT model --------------------
"""


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


"""
------------------- End : Implementation of TALENT model --------------------
"""


"""
------------------- Start : Implementation of HIRE_EVENT model --------------------
"""


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


"""
------------------- End : Implementation of HIRE_EVENT model --------------------
"""


"""
------------------- Start : Implementation of HIRE_EVENT_TYPE model --------------------
"""


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


"""
------------------- Start : Implementation of RESUME model --------------------
"""


class ResumeList(APIView):

    def get(self, request):
        """
        List all resumes.
        """
        resumes = Resume.objects.all()
        serializer = ResumeMiniSerializer(resumes, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new resume instance
        """
        serializer = ResumeMiniSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResumeDetail(APIView):

    def get_object(self, pk):
        try:
            return Resume.objects.get(pk=pk)
        except Resume.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        Retrieve a resume instance.
        """
        resume = self.get_object(pk)
        serializer = ResumeMiniSerializer(resume)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update a resume instance
        """
        resume = self.get_object(pk)
        serializer = ResumeMiniSerializer(resume, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    def delete(self, request, pk):
        resume = self.get_object(pk)
        resume.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    """


"""
------------------- End : Implementation of RESUME model --------------------
"""


"""
------------------- Start : Implementation of JOB_EXPERIENCE model --------------------
"""


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


"""
------------------- End : Implementation of JOB_EXPERIENCE model --------------------
"""


"""
------------------- Start : Implementation of TECHNICAL_SKILL model --------------------
"""


class TechnicalSkillList(APIView):

    def get(self, request):
        """
        List all technical skills.
        """
        technical_skills = TechnicalSkill.objects.all()
        serializer = TechnicalSkillSerializer(technical_skills, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new technical skill instance.
        """
        serializer = TechnicalSkillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TechnicalSkillDetail(APIView):

    def get_object(self, pk):
        try:
            return TechnicalSkill.objects.get(pk=pk)
        except TechnicalSkill.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        Retrieve a technical skill instance.
        """
        technical_skill = self.get_object(pk)
        serializer = TechnicalSkillSerializer(technical_skill)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update a technical skill instance
        """
        technical_skill = self.get_object(pk)
        serializer = TechnicalSkillSerializer(technical_skill, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    def delete(self, request, pk):
        technical_skill = self.get_object(pk)
        technical_skill.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    """


"""
------------------- End : Implementation of TECHNICAL_SKILL model --------------------
"""

"""
------------------- Start : Implementation of EDUCATION model --------------------
"""


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


"""
------------------- End : Implementation of EDUCATION model --------------------
"""

"""
------------------- Start : Implementation of LANGUAGE_SKILL model --------------------
"""


class LanguageSkillList(APIView):

    def get(self, request):
        """
        List all language skills.
        """
        language_skills = LanguageSkill.objects.all()
        serializer = LanguageSkillSerializer(language_skills, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new language skill instance
        """
        serializer = LanguageSkillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LanguageSkillDetail(APIView):

    def get_object(self, pk):
        try:
            return LanguageSkill.objects.get(pk=pk)
        except LanguageSkill.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        Retrieve a language skill instance.
        """
        language_skill = self.get_object(pk)
        serializer = LanguageSkillSerializer(language_skill)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update a language skill instance.
        """
        language_skill = self.get_object(pk)
        serializer = LanguageSkillSerializer(language_skill, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    def delete(self, request, pk):
        language_skill = self.get_object(pk)
        language_skill.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    """


"""
------------------- End : Implementation of LANGUAGE_SKILL model --------------------
"""

"""
------------------- Start : Implementation of ADDRESS model --------------------
"""


class AddressList(APIView):

    def get(self, request):
        """
        List all addresses.
        """
        addresses = Address.objects.all()
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new address instance.
        """
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressDetail(APIView):

    def get_object(self, pk):
        try:
            return Address.objects.get(pk=pk)
        except Address.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        Retrieve an address instance.
        """
        address = self.get_object(pk)
        serializer = AddressSerializer(address)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update an address instance.
        """
        address = self.get_object(pk)
        serializer = AddressSerializer(address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    def delete(self, request, pk):
        address = self.get_object(pk)
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    """


"""
------------------- End : Implementation of ADDRESS model --------------------
"""


"""
------------------- Start : Implementation of EXPERTISE model --------------------
"""


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


"""
------------------- End : Implementation of EXPERTISE model --------------------
"""


"""
------------------- Start : Implementation of RECRUITER model --------------------
"""


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


"""
------------------- End : Implementation of RECRUITER model --------------------
"""
