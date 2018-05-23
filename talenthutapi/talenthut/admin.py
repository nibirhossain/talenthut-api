"""
from django.contrib import admin
import nested_admin

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from .models import Talent, Address, Expertise, Resume
from .models import JobExperience, TechnicalSkill, Education, LanguageSkill
from .models import Recruiter, HireEvent, HireEventType


class AddressInline(nested_admin.NestedTabularInline):
    model = Address
    extra = 1


class JobExperienceInline(nested_admin.NestedTabularInline):
    model = JobExperience
    extra = 1


class EducationInline(nested_admin.NestedTabularInline):
    model = Education
    extra = 1


class TechnicalSkillInline(nested_admin.NestedTabularInline):
    model = TechnicalSkill
    extra = 1


class LanguageSkillInline(nested_admin.NestedTabularInline):
    model = LanguageSkill
    extra = 1


class ResumeInline(nested_admin.NestedTabularInline):
    model = Resume
    inlines = [JobExperienceInline, EducationInline, TechnicalSkillInline, LanguageSkillInline]


class TalentAdmin(nested_admin.NestedModelAdmin):
    fieldsets = [
        (None,               {'fields': ['firstname', 'lastname', 'sex', 'marital_status', 'birthdate', 'email', 'mobile', 'qualification', 'birthplace', 'photo',
        'experience', 'expertises', 'description']}),
    ]
    inlines = [AddressInline, ResumeInline]


admin.site.register(Talent, TalentAdmin)
admin.site.register(Expertise)


class RecruiterInline(nested_admin.NestedTabularInline):
    model = Recruiter
    can_delete = False
    verbose_name_plural = 'Recruiter'
    fk_name = 'user'


class RecruiterAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name',
        'is_active', 'is_staff', 'date_joined', 'last_login')
    list_filter = ('is_active', 'is_staff', 'is_superuser',
        'date_joined', 'last_login')
    ordering = ('last_name', 'first_name', 'username')
    save_on_top = True
    inlines = [RecruiterInline]


admin.site.unregister(User)
admin.site.register(User, RecruiterAdmin)
admin.site.register(HireEvent)
admin.site.register(HireEventType)
"""

# django framework specific
from django.contrib import admin

# project specific
from .models import Talent, Address, Expertise, Resume
from .models import JobExperience, TechnicalSkill, Education, LanguageSkill
from .models import Recruiter, RecruiterActivity, RecruiterEvent, Sex, MaritalStatus

admin.site.register(Sex)
admin.site.register(MaritalStatus)
admin.site.register(Talent)
admin.site.register(Address)
admin.site.register(Expertise)
admin.site.register(Resume)
admin.site.register(JobExperience)
admin.site.register(TechnicalSkill)
admin.site.register(Education)
admin.site.register(LanguageSkill)

# admin.site.unregister(User)
admin.site.register(Recruiter)
admin.site.register(RecruiterActivity)
admin.site.register(RecruiterEvent)