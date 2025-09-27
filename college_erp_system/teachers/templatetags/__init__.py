from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary by key"""
    return dictionary.get(key, [])

@register.filter
def sum_student_counts(classes_list):
    """Sum up student counts from classes"""
    total = 0
    for class_info in classes_list:
        if hasattr(class_info, 'student_count'):
            total += class_info['student_count'] if isinstance(class_info, dict) else class_info.student_count
    return total