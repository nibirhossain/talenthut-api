from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Here models are created for talenthut system
class Sex(models.Model):
    gender = models.CharField(max_length=10, default='')

    class Meta:
        verbose_name = 'Sex'
        verbose_name_plural = 'Sexes'

    def __str__(self):
        return self.gender


class MaritalStatus(models.Model):
    status = models.CharField(max_length=20, default='')

    class Meta:
        verbose_name = 'Marital Status'
        verbose_name_plural = 'Marital Statuses'

    def __str__(self):
        return self.status


class Talent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sex = models.ForeignKey(Sex, on_delete=models.CASCADE)
    marital_status = models.ForeignKey(MaritalStatus, on_delete=models.CASCADE)
    experience = models.FloatField(default=0)
    birthdate = models.DateField(default='1900-01-01')
    mobile = models.CharField(max_length=20, default='')
    qualification = models.CharField(max_length=100, verbose_name='Qualification')
    birthplace = models.CharField(max_length=100, verbose_name='Birth Place')
    photo = models.ImageField(upload_to="static/talent/img/", null=True, blank=True)
    expertises = models.ManyToManyField('Expertise')
    description = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Expertise(models.Model):
    expertise_in = models.CharField(max_length=50)

    def __str__(self):
        return self.expertise_in


class Address(models.Model):
    talent = models.ForeignKey(Talent, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return self.city


class Resume(models.Model):
    talent = models.OneToOneField(Talent, on_delete=models.CASCADE)
    description = models.TextField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = 'Resume'
        verbose_name_plural = 'Resumes'

    def __str__(self):
        return self.description


class JobExperience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    start_date = models.DateField(blank=True, null=True, verbose_name='Start Date')
    end_date = models.DateField(blank=True, null=True, verbose_name='End Date')
    position = models.CharField(max_length=50)
    company = models.CharField(max_length=50)
    website = models.URLField(max_length=200, null=True, blank=True, verbose_name='Company Website')

    class Meta:
        verbose_name = 'Job Experience'
        verbose_name_plural = 'Job Experiences'
        ordering = ['-start_date']

    def __str__(self):
        return self.position


class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    start_date = models.DateField(blank=True, null=True, verbose_name='Start Date')
    completion_date = models.DateField(blank=True, null=True, verbose_name='Completion Date')
    graduation = models.CharField(max_length=50, verbose_name='Graduation')
    organization = models.CharField(max_length=100, verbose_name='Organization')
    website = models.URLField(max_length=200, null=True, blank=True, verbose_name='Organization Website')

    class Meta:
        verbose_name = 'Education'
        verbose_name_plural = 'Education'
        ordering = ['-start_date']

    def __str__(self):
        return self.graduation


class TechnicalSkill(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    skill_title = models.CharField(max_length=100, null=True, verbose_name='Skill Title')
    skill_list = models.CharField(max_length=100, null=True, verbose_name='List of Skills')

    class Meta:
        verbose_name = 'Technical Skill'
        verbose_name_plural = 'Technical Skills'
        ordering = ['id']

    def __str__(self):
        return self.skill_title


class LanguageSkill(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True, verbose_name='Language Name')
    skill_level = models.CharField(max_length=50, verbose_name='Skill Level')

    class Meta:
        verbose_name = 'Language Skill'
        verbose_name_plural = 'Language Skills'

    def __str__(self):
        return self.name


# Here models are created for Recruiter
class Recruiter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=50)
    company_website = models.URLField(max_length=200, null=True, blank=True, verbose_name='Company Website')
    position = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Recruiter'
        verbose_name_plural = 'Recruiters'
        # ordering = ['first_name', 'last_name']

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


class HireEvent(models.Model):
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    talent = models.ForeignKey(Talent, on_delete=models.CASCADE)
    hire_event_type = models.ForeignKey('HireEventType', on_delete=models.CASCADE)
    event_time = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Hire Event'
        verbose_name_plural = 'Hire Events'
        # ordering = ['-event_time']
        ordering = ['talent__user__first_name', 'talent__user__last_name', 'talent__id', '-event_time']
        unique_together = ['recruiter', 'talent', 'hire_event_type']

    def __str__(self):
        return 'HireEvent id ' + str(self.hire_event_type.id)


class HireEventType(models.Model):
    name = models.CharField(max_length=30, unique=True, default='')
    message = models.CharField(max_length=300, default='')
    icon = models.ImageField(upload_to="static/img/", default='')
    description = models.CharField(max_length=30, default='')

    class Meta:
        verbose_name = 'Hire Event Type'
        verbose_name_plural = 'Hire Event Types'

    def __str__(self):
        return self.name