"""
Context processors for College ERP System
"""
from college_erp.config import InstitutionConfig, AcademicConfig


def institution_context(request):
    """
    Add institution configuration to template context
    """
    return {
        'INSTITUTION': InstitutionConfig,
        'ACADEMIC_CONFIG': AcademicConfig,
    }


def user_context(request):
    """
    Add user-specific context data
    """
    if request.user.is_authenticated:
        return {
            'current_user': request.user,
        }
    return {}