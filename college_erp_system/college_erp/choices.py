"""
Dynamic choices for College ERP System
This module provides database-driven choices instead of hardcoded values
"""
from django.db import models


class ChoiceCategory(models.Model):
    """Categories for different types of choices"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Choice Categories'
    
    def __str__(self):
        return self.name


class Choice(models.Model):
    """Dynamic choices for various fields"""
    category = models.ForeignKey(ChoiceCategory, on_delete=models.CASCADE, related_name='choices')
    value = models.CharField(max_length=50)  # The actual value stored in database
    label = models.CharField(max_length=100)  # The display name
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)  # For ordering choices
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'order', 'label']
        unique_together = ['category', 'value']
    
    def __str__(self):
        return f"{self.category.name}: {self.label}"
    
    @classmethod
    def get_choices_for_category(cls, category_name):
        """Get choices as tuples for Django model field choices"""
        try:
            category = ChoiceCategory.objects.get(name=category_name)
            return list(
                cls.objects.filter(category=category, is_active=True)
                .order_by('order', 'label')
                .values_list('value', 'label')
            )
        except ChoiceCategory.DoesNotExist:
            return []
    
    @classmethod
    def get_choice_dict_for_category(cls, category_name):
        """Get choices as dictionary for templates"""
        try:
            category = ChoiceCategory.objects.get(name=category_name)
            return {
                choice.value: choice.label 
                for choice in cls.objects.filter(category=category, is_active=True)
                .order_by('order', 'label')
            }
        except ChoiceCategory.DoesNotExist:
            return {}


# Helper functions to get dynamic choices
def get_user_type_choices():
    """Get user type choices from database"""
    try:
        return Choice.get_choices_for_category('user_types')
    except Exception:
        return []

def get_notification_type_choices():
    """Get notification type choices from database"""
    try:
        return Choice.get_choices_for_category('notification_types')
    except Exception:
        return []

def get_qualification_choices():
    """Get qualification choices from database"""
    try:
        return Choice.get_choices_for_category('qualifications')
    except Exception:
        return []

def get_employment_type_choices():
    """Get employment type choices from database"""
    try:
        return Choice.get_choices_for_category('employment_types')
    except Exception:
        return []

def get_semester_choices():
    """Get semester choices from database"""
    try:
        return Choice.get_choices_for_category('semesters')
    except Exception:
        return []

def get_fee_type_choices():
    """Get fee type choices from database"""
    try:
        return Choice.get_choices_for_category('fee_types')
    except Exception:
        return []

def get_payment_status_choices():
    """Get payment status choices from database"""
    try:
        return Choice.get_choices_for_category('payment_status')
    except Exception:
        return []

def get_exam_type_choices():
    """Get exam type choices from database"""
    try:
        return Choice.get_choices_for_category('exam_types')
    except Exception:
        return []

def get_priority_choices():
    """Get priority choices from database"""
    try:
        return Choice.get_choices_for_category('priority_levels')
    except Exception:
        return []

def get_recipient_type_choices():
    """Get recipient type choices from database"""
    try:
        return Choice.get_choices_for_category('recipient_types')
    except Exception:
        return []

def get_day_choices():
    """Get day choices from database"""
    try:
        return Choice.get_choices_for_category('weekdays')
    except Exception:
        return []

def get_target_audience_choices():
    """Get target audience choices from database"""
    try:
        return Choice.get_choices_for_category('target_audience')
    except Exception:
        return []