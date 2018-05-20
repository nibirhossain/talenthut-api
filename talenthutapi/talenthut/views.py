from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status

from django.contrib.auth.models import User

from .models import Talent, Address, Expertise, Resume
from .models import JobExperience, TechnicalSkill, Education, LanguageSkill
from .models import Recruiter, HireEvent, HireEventType

from .resume_serializers import HireEventTypeSerializer, ExpertiseSerializer
from .hire_event_serializers import HireEventListAndDetailSerializer
from .resume_serializers import AddressSerializer, JobExperienceSerializer
from .resume_serializers import TechnicalSkillSerializer, EducationSerializer, LanguageSkillSerializer
from .resume_serializers import ResumeSerializer
from .user_serializers import UserSerializer
from .talent_serializers import TalentListSerializer, TalentSerializer
from .recruiter_serializers import RecruiterSerializer, RecruiterCreateSerializer, RecruiterUpdateSerializer


class UserList(APIView):
    """
    List all talents by recruiter using hire event type.
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
    Retrieve, update or delete a snippet instance.
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
    List all talents or create a new talent.
    """

    def get(self, request):
        talents = Talent.objects.all()
        serializer = TalentSerializer(talents, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TalentSerializer(data=request.data)
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


class TalentListByRecruiter(APIView):
    """
    List all talents by recruiter.
    """

    def get(self, request, recruiter_pk):

        # distinct is not supported on sqlite3 database
        # hire_events = HireEvent.objects.filter(recruiter=recruiter_pk) \
        # .order_by('talent__user__firstname', 'talent__user__lastname', 'talent__id', '-event_time') \
        #     .distinct('talent__fuser__irstname', 'talent__user__lastname', 'talent__id')

        # since sqlite3 does not support the distinct property, talents could be duplicated. Fix it later.
        hire_events = HireEvent.objects.filter(recruiter=recruiter_pk) \
        .order_by('talent__user__first_name', 'talent__user__last_name', 'talent__id', '-event_time')

        talents = [hire_event.talent for hire_event in hire_events]
        serializer = TalentListSerializer(talents, many=True)

        return Response(serializer.data)


class TalentListByRecruiterUsingHireEventType(APIView):
    """
    List all talents by recruiter using hire event type.
    """
    def get(self, request, recruiter_pk, event_type_pk):
        hire_events = HireEvent.objects.filter(recruiter=recruiter_pk, hire_event_type_id=event_type_pk) \
            .order_by('talent__user__first_name', 'talent__user__last_name')

        talents = [hire_event.talent for hire_event in hire_events]
        serializer = TalentListSerializer(talents, many=True)

        return Response(serializer.data)


class TalentDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self, pk):
        try:
            return Talent.objects.get(pk=pk)
        except Talent.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        talent = self.get_object(pk)
        serializer = TalentSerializer(talent)
        return Response(serializer.data)

    def put(self, request, pk):
        talent = self.get_object(pk)
        serializer = TalentSerializer(talent, data=request.data)
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


class HireEventList(APIView):
    """
    List all hire event type, or create a new hire event type.
    """
    def get(self, request):
        hire_events = HireEvent.objects.all()
        serializer = HireEventListAndDetailSerializer(hire_events, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = HireEventListAndDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HireEventDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self, pk):
        try:
            return HireEvent.objects.get(pk=pk)
        except HireEvent.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        hire_event = self.get_object(pk)
        serializer = HireEventListAndDetailSerializer(hire_event)
        return Response(serializer.data)

    def put(self, request, pk):
        hire_event = self.get_object(pk)
        serializer = HireEventListAndDetailSerializer(hire_event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        hire_event = self.get_object(pk)
        hire_event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""
------------------- End : Implementation of HIRE_EVENT model --------------------
"""


"""
------------------- Start : Implementation of HIRE_EVENT_TYPE model --------------------
"""


class HireEventTypeList(APIView):
    """
    List all hire event type, or create a new hire event type.
    """
    def get(self, request):
        hire_event_types = HireEventType.objects.all()
        serializer = HireEventTypeSerializer(hire_event_types, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = HireEventTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HireEventTypeDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self, pk):
        try:
            return HireEventType.objects.get(pk=pk)
        except HireEventType.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        hire_event_type = self.get_object(pk)
        serializer = HireEventTypeSerializer(hire_event_type)
        return Response(serializer.data)

    def put(self, request, pk):
        hire_event_type = self.get_object(pk)
        serializer = HireEventTypeSerializer(hire_event_type, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        hire_event_type = self.get_object(pk)
        hire_event_type.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""
------------------- End : Implementation of HIRE_EVENT_TYPE model --------------------
"""


"""
------------------- Start : Implementation of RESUME model --------------------
"""


class ResumeList(APIView):
    """
    List all hire event type, or create a new hire event type.
    """

    def get(self, request):
        resumes = Resume.objects.all()
        serializer = ResumeSerializer(resumes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ResumeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResumeDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self, pk):
        try:
            return Resume.objects.get(pk=pk)
        except Resume.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        resume = self.get_object(pk)
        serializer = ResumeSerializer(resume)
        return Response(serializer.data)

    def put(self, request, pk):
        resume = self.get_object(pk)
        serializer = ResumeSerializer(resume, data=request.data)
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
    List all hire event type, or create a new hire event type.
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
    Retrieve, update or delete a snippet instance.
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
    List all hire event type, or create a new hire event type.
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
    Retrieve, update or delete a snippet instance.
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
    List all hire event type, or create a new hire event type.
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
    Retrieve, update or delete a snippet instance.
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
    List all hire event type, or create a new hire event type.
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
    Retrieve, update or delete a snippet instance.
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
    List all hire event type, or create a new hire event type.
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
    Retrieve, update or delete a snippet instance.
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
    List all hire event type, or create a new hire event type.
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
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self, pk):
        try:
            return Expertise.objects.get(pk=pk)
        except Expertise.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        expertise = self.get_object(pk)
        serializer = HireEventTypeSerializer(expertise)
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
    List all hire event type, or create a new hire event type.
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
    Retrieve, update or delete a snippet instance.
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
