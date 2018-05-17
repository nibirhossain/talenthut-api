from django.urls import path

from .views import HireEventTypeList, HireEventTypeDetail
from .views import ExpertiseList, ExpertiseDetail
from .views import TalentList, TalentDetail
from .views import AddressList, AddressDetail
from .views import ResumeList, ResumeDetail
from .views import JobExperienceList, JobExperienceDetail
from .views import TechnicalSkillList, TechnicalSkillDetail
from .views import EducationList, EducationDetail
from .views import LanguageSkillList, LanguageSkillDetail
from .views import HireEventList, HireEventDetail
from .views import RecruiterList, RecruiterDetail
from .views import TalentListByExpertise, TalentListByRecruiter
from .views import TalentListByRecruiterUsingHireEventType
from .views import UserList, UserDetail


# from . import views as views_talenthut

app_name = 'talenthut'

urlpatterns = [
    # ex: /
    # path('', IndexView.as_view(), name='index'),
    # path('talents/', views_talenthut.TalentListView.as_view(), name='list'),
    # path('talent-list-by-expertise/<int:expertise_id>/', views_talenthut.TalentListViewByExpertise.as_view(), name='list_by_expertise'),
    # path('talent/<int:pk>/', views_talenthut.TalentDetailView.as_view(), name='detail'),

    path('hire-event-types/', HireEventTypeList.as_view(), name="hire_event_type_list"),
    path('hire-event-types/<pk>/', HireEventTypeDetail.as_view(), name="hire_event_type_detail"),

    path('expertises/', ExpertiseList.as_view(), name="expertise_list"),
    path('expertises/<pk>/', ExpertiseDetail.as_view(), name="expertise_detail"),
    path('expertises/<int:expertise_pk>/talents/', TalentListByExpertise.as_view(), name="talent_list_by_expertise"),

    path('users/', UserList.as_view(), name="user_list"),
    path('users/<pk>/', UserDetail.as_view(), name="user_detail"),

    path('talents/', TalentList.as_view(), name="talent_list"),
    path('talents/<pk>/', TalentDetail.as_view(), name="talent_detail"),

    path('addresses/', AddressList.as_view(), name="address_list"),
    path('addresses/<pk>/', AddressDetail.as_view(), name="address_detail"),

    path('resumes/', ResumeList.as_view(), name="resume_list"),
    path('resumes/<pk>/', ResumeDetail.as_view(), name="resume_detail"),

    path('job-experiences/', JobExperienceList.as_view(), name="job_experience_list"),
    path('job-experiences/<pk>/', JobExperienceDetail.as_view(), name="job_experience_detail"),

    path('technical-skills/', TechnicalSkillList.as_view(), name="technical_skill_list"),
    path('technical-skills/<pk>/', TechnicalSkillDetail.as_view(), name="technical_skill_detail"),

    path('educations/', EducationList.as_view(), name="education_list"),
    path('educations/<pk>/', EducationDetail.as_view(), name="education_detail"),

    path('language-skills/', LanguageSkillList.as_view(), name="language_skill_list"),
    path('language-skills/<pk>/', LanguageSkillDetail.as_view(), name="language_skill_detail"),

    path('hire-events/', HireEventList.as_view(), name="hire_event_list"),
    path('hire-events/<pk>/', HireEventDetail.as_view(), name="hire_event_detail"),

    path('recruiters/', RecruiterList.as_view(), name="recruiter_list"),
    path('recruiters/<pk>/', RecruiterDetail.as_view(), name="recruiter_detail"),
    path('recruiters/<int:recruiter_pk>/talents/', TalentListByRecruiter.as_view(), name="talent_list_by_recruiter"),
    path('recruiters/<int:recruiter_pk>/event-types/<int:event_type_pk>/talents/',
         TalentListByRecruiterUsingHireEventType.as_view(), name="talent_list_by_recruiter_using_hire_event_type"),

]
