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