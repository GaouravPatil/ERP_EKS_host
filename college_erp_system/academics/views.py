from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from college_erp.config import InstitutionConfig, AppConfig

@login_required
def index(request):
    """Academic module main index view"""
    user = request.user
    
    context = {
        'user': user,
        'institution_name': InstitutionConfig.NAME,
        'welcome_message': f"Welcome to {InstitutionConfig.NAME} Academic System",
        'user_permissions': AppConfig.DEFAULT_STUDENT_PERMISSIONS if user.is_student 
                          else AppConfig.DEFAULT_TEACHER_PERMISSIONS if user.is_teacher 
                          else []
    }
    
    return render(request, 'academics/index.html', context)
