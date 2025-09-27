from django.urls import path
from . import views

app_name = 'teachers'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('timetable/', views.timetable_view, name='timetable'),
    path('attendance/', views.attendance_view, name='attendance'),
    path('mark-attendance/', views.mark_attendance, name='mark_attendance'),
    path('exams/', views.exams_view, name='exams'),
    path('grades/', views.grades_view, name='grades'),
    path('classes/', views.classes_view, name='classes'),
]
