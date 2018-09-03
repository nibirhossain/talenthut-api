from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from ..models import LanguageSkill
from ..th_serializers.resume import LanguageSkillSerializer


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
