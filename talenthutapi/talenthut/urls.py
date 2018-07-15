from django.urls import path

from .views import RecruiterEventList, RecruiterEventDetail
from .views import ExpertiseList, ExpertiseDetail
from .views import TalentList, TalentDetail
from .views import AddressList, AddressDetail
from .views import ResumeList, ResumeDetail
from .views import JobExperienceList, JobExperienceDetail
from .views import TechnicalSkillList, TechnicalSkillDetail
from .views import EducationList, EducationDetail
from .views import LanguageSkillList, LanguageSkillDetail
from .views import RecruiterActivities, RecruiterActivityDetail
from .views import RecruiterList, RecruiterDetail
from .views import TalentListByExpertise, RecruiterActivityList
from .views import RecruiterActivityListByRecruiterEvent
from .views import UserList, UserDetail
from .views import HomeView

app_name = 'talenthut'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('recruiter-events/', RecruiterEventList.as_view(), name="recruiter_event_list"),
    path('recruiter-events/<pk>/', RecruiterEventDetail.as_view(), name="recruiter_event_detail"),

    # path('expertises/', ExpertiseList.as_view(), name="expertise_list"),
    # path('expertises/<pk>/', ExpertiseDetail.as_view(), name="expertise_detail"),

    path('users/', UserList.as_view(), name="user_list"),
    path('users/<pk>/', UserDetail.as_view(), name="user_detail"),

    path('talents/', TalentList.as_view(), name="talent_list"),
    path('talents/<pk>/', TalentDetail.as_view(), name="talent_detail"),
    path('talents/expertises/<int:expertise_pk>/', TalentListByExpertise.as_view(), name="talent_list_by_expertise"),

    # path('addresses/', AddressList.as_view(), name="address_list"),
    # path('addresses/<pk>/', AddressDetail.as_view(), name="address_detail"),

    # path('resumes/', ResumeList.as_view(), name="resume_list"),
    # path('resumes/<pk>/', ResumeDetail.as_view(), name="resume_detail"),

    # path('job-experiences/', JobExperienceList.as_view(), name="job_experience_list"),
    # path('job-experiences/<pk>/', JobExperienceDetail.as_view(), name="job_experience_detail"),

    # path('technical-skills/', TechnicalSkillList.as_view(), name="technical_skill_list"),
    # path('technical-skills/<pk>/', TechnicalSkillDetail.as_view(), name="technical_skill_detail"),

    # path('educations/', EducationList.as_view(), name="education_list"),
    # path('educations/<pk>/', EducationDetail.as_view(), name="education_detail"),

    # path('language-skills/', LanguageSkillList.as_view(), name="language_skill_list"),
    # path('language-skills/<pk>/', LanguageSkillDetail.as_view(), name="language_skill_detail"),

    path('recruiters/', RecruiterList.as_view(), name="recruiter_list"),
    path('recruiters/<pk>/', RecruiterDetail.as_view(), name="recruiter_detail"),

    path('recruiter-activities/', RecruiterActivities.as_view(), name="recruiter_activities_list"),
    path('recruiter-activities/<pk>/', RecruiterActivityDetail.as_view(), name="recruiter_activity_detail"),
    path('recruiter-activities/recruiters/<int:recruiter_pk>/talents/', RecruiterActivityList.as_view(),
         name="talent_list_by_recruiter"),
    path('recruiter-activities/<int:recruiter_event_pk>/recruiters/<int:recruiter_pk>/talents/',
         RecruiterActivityListByRecruiterEvent.as_view(), name="recruiter_activity_list_by_recruiter_event"),

]
