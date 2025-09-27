from django.db import models
from django.conf import settings
from academics.models import Department


def get_qualification_choices():
    """Get qualification choices from database"""
    from college_erp.models import Choice
    return Choice.get_choices_for_category('qualifications')


def get_employment_type_choices():
    """Get employment type choices from database"""
    from college_erp.models import Choice
    return Choice.get_choices_for_category('employment_types')


class Teacher(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='teacher_profile'
    )
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    designation = models.CharField(max_length=100)
    qualification = models.CharField(max_length=20, choices=get_qualification_choices)
    specialization = models.CharField(max_length=200, blank=True)
    experience_years = models.IntegerField(default=0)
    employment_type = models.CharField(max_length=20, choices=get_employment_type_choices)
    joining_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    office_room = models.CharField(max_length=50, blank=True)
    office_hours = models.CharField(max_length=100, blank=True)
    research_interests = models.TextField(blank=True)
    publications = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.employee_id} - {self.user.get_full_name()}"
    
    @property
    def full_name(self):
        return self.user.get_full_name()
