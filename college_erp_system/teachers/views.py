from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from datetime import datetime, timedelta
from collections import defaultdict

from .models import Teacher
from academics.models import (
    Subject, Class, Timetable, Attendance, 
    Exam, Result, TimeSlot
)
from students.models import Student
from administration.models import Notification
from college_erp.config import TimeConfig

@login_required
def dashboard(request):
    """Teacher Dashboard View"""
    try:
        teacher = request.user.teacher_profile
    except Teacher.DoesNotExist:
        messages.error(request, "Teacher profile not found. Please contact administration.")
        return redirect('accounts:login')
    
    # Get current date info
    today = timezone.now().date()
    current_time = timezone.now().time()
    
    # Get teacher's subjects and classes
    taught_subjects = Subject.objects.filter(teacher=request.user).select_related(
        'course', 'class_assigned', 'class_assigned__department'
    )
    
    # Get today's timetable
    today_classes = Timetable.objects.filter(
        subject__teacher=request.user,
        time_slot__day=today.strftime('%A').lower()
    ).select_related('subject', 'class_assigned', 'time_slot').order_by('time_slot__start_time')
    
    # Get recent notifications
    recent_notifications = Notification.objects.filter(
        Q(recipient_type='all') | 
        Q(recipient_type='teachers') |
        Q(sender=request.user)
    ).filter(is_active=True).order_by('-created_at')[:5]
    
    # Get upcoming exams
    upcoming_exams = Exam.objects.filter(
        subject__teacher=request.user,
        date__gte=timezone.now()
    ).select_related('subject', 'subject__course').order_by('date')[:5]
    
    # Get pending results to publish
    pending_results = Result.objects.filter(
        exam__subject__teacher=request.user,
        is_published=False
    ).select_related('exam', 'student').count()
    
    # Attendance statistics
    total_students = Student.objects.filter(
        student_class__in=[subject.class_assigned for subject in taught_subjects]
    ).count()
    
    # Today's attendance summary
    today_attendance = Attendance.objects.filter(
        subject__teacher=request.user,
        date=today
    ).aggregate(
        present=Count('id', filter=Q(is_present=True)),
        absent=Count('id', filter=Q(is_present=False))
    )
    
    # Next class info
    next_class = None
    for timetable in today_classes:
        if timetable.time_slot.start_time > current_time:
            next_class = timetable
            break
    
    context = {
        'teacher': teacher,
        'taught_subjects': taught_subjects,
        'today_classes': today_classes,
        'recent_notifications': recent_notifications,
        'upcoming_exams': upcoming_exams,
        'pending_results': pending_results,
        'total_students': total_students,
        'today_attendance': today_attendance,
        'next_class': next_class,
        'today': today,
    }
    
    return render(request, 'teachers/dashboard.html', context)

@login_required
def timetable_view(request):
    """Teacher Timetable View"""
    try:
        teacher = request.user.teacher_profile
    except Teacher.DoesNotExist:
        messages.error(request, "Teacher profile not found.")
        return redirect('teachers:dashboard')
    
    # Get all timetable entries for this teacher
    timetable_entries = Timetable.objects.filter(
        subject__teacher=request.user
    ).select_related(
        'subject__course', 'class_assigned', 'time_slot'
    ).order_by('time_slot__day', 'time_slot__start_time')
    
    # Define standard time slots using config
    standard_time_slots = TimeConfig.STANDARD_TIME_SLOTS
    
    # Organize by day and time using config
    days = TimeConfig.WEEKDAYS
    
    # Create organized timetable structure
    organized_timetable = {}
    for day_key, day_name in days:
        organized_timetable[day_key] = {}
        day_entries = timetable_entries.filter(time_slot__day=day_key)
        
        for entry in day_entries:
            time_key = f"{entry.time_slot.start_time}_{entry.time_slot.end_time}"
            organized_timetable[day_key][time_key] = entry
    
    # Get all unique time slots from the teacher's schedule
    teacher_time_slots = TimeSlot.objects.filter(
        timetable__subject__teacher=request.user
    ).distinct().order_by('start_time')
    
    # If no specific slots, use standard ones that exist in database
    if not teacher_time_slots.exists():
        teacher_time_slots = TimeSlot.objects.all().order_by('start_time')[:9]
    
    context = {
        'teacher': teacher,
        'organized_timetable': organized_timetable,
        'time_slots': teacher_time_slots,
        'standard_time_slots': standard_time_slots,
        'days': days,
        'timetable_entries': timetable_entries,
    }
    
    return render(request, 'teachers/timetable.html', context)

@login_required
def attendance_view(request):
    """Teacher Attendance Management"""
    try:
        teacher = request.user.teacher_profile
    except Teacher.DoesNotExist:
        messages.error(request, "Teacher profile not found.")
        return redirect('teachers:dashboard')
    
    # Get teacher's subjects
    subjects = Subject.objects.filter(teacher=request.user).select_related(
        'course', 'class_assigned'
    )
    
    selected_subject_id = request.GET.get('subject')
    selected_date = request.GET.get('date', timezone.now().date().isoformat())
    
    selected_subject = None
    students_attendance = []
    
    if selected_subject_id:
        selected_subject = get_object_or_404(Subject, id=selected_subject_id, teacher=request.user)
        
        # Get students in this class
        students = Student.objects.filter(
            student_class=selected_subject.class_assigned,
            is_active=True
        ).select_related('user').order_by('roll_number')
        
        # Get attendance records for selected date
        attendance_records = Attendance.objects.filter(
            subject=selected_subject,
            date=selected_date
        )
        
        attendance_dict = {record.student.id: record for record in attendance_records}
        
        for student in students:
            attendance_record = attendance_dict.get(student.user.id)
            students_attendance.append({
                'student': student,
                'attendance': attendance_record,
                'is_present': attendance_record.is_present if attendance_record else False
            })
    
    context = {
        'teacher': teacher,
        'subjects': subjects,
        'selected_subject': selected_subject,
        'selected_date': selected_date,
        'students_attendance': students_attendance,
    }
    
    return render(request, 'teachers/attendance.html', context)

@login_required
@require_POST
def mark_attendance(request):
    """Mark attendance for students"""
    try:
        teacher = request.user.teacher_profile
    except Teacher.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Teacher profile not found.'})
    
    subject_id = request.POST.get('subject_id')
    date = request.POST.get('date')
    attendance_data = request.POST.getlist('attendance')
    
    try:
        subject = Subject.objects.get(id=subject_id, teacher=request.user)
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        
        # Clear existing attendance for this date and subject
        Attendance.objects.filter(subject=subject, date=date_obj).delete()
        
        # Create new attendance records
        students = Student.objects.filter(
            student_class=subject.class_assigned,
            is_active=True
        )
        
        for student in students:
            is_present = str(student.user.id) in attendance_data
            Attendance.objects.create(
                student=student.user,
                subject=subject,
                date=date_obj,
                is_present=is_present,
                marked_by=request.user
            )
        
        return JsonResponse({'success': True, 'message': 'Attendance marked successfully!'})
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@login_required
def exams_view(request):
    """Teacher Exams Management"""
    try:
        teacher = request.user.teacher_profile
    except Teacher.DoesNotExist:
        messages.error(request, "Teacher profile not found.")
        return redirect('teachers:dashboard')
    
    # Get all exams created by this teacher
    exams = Exam.objects.filter(
        subject__teacher=request.user
    ).select_related('subject__course', 'subject__class_assigned').order_by('-date')
    
    # Separate upcoming and past exams
    now = timezone.now()
    upcoming_exams = exams.filter(date__gte=now)
    past_exams = exams.filter(date__lt=now)
    
    context = {
        'teacher': teacher,
        'upcoming_exams': upcoming_exams,
        'past_exams': past_exams,
    }
    
    return render(request, 'teachers/exams.html', context)

@login_required
def grades_view(request):
    """Teacher Grades Management"""
    try:
        teacher = request.user.teacher_profile
    except Teacher.DoesNotExist:
        messages.error(request, "Teacher profile not found.")
        return redirect('teachers:dashboard')
    
    # Get teacher's subjects
    subjects = Subject.objects.filter(teacher=request.user).select_related(
        'course', 'class_assigned'
    )
    
    selected_exam_id = request.GET.get('exam')
    selected_exam = None
    results = []
    
    if selected_exam_id:
        selected_exam = get_object_or_404(Exam, id=selected_exam_id, subject__teacher=request.user)
        
        # Get all results for this exam
        results = Result.objects.filter(exam=selected_exam).select_related(
            'student__student_profile'
        ).order_by('student__student_profile__roll_number')
    
    # Get all exams for this teacher
    exams = Exam.objects.filter(
        subject__teacher=request.user
    ).select_related('subject__course').order_by('-date')
    
    context = {
        'teacher': teacher,
        'subjects': subjects,
        'exams': exams,
        'selected_exam': selected_exam,
        'results': results,
    }
    
    return render(request, 'teachers/grades.html', context)

@login_required
def classes_view(request):
    """Teacher Classes Management"""
    try:
        teacher = request.user.teacher_profile
    except Teacher.DoesNotExist:
        messages.error(request, "Teacher profile not found.")
        return redirect('teachers:dashboard')
    
    # Get all classes taught by this teacher
    taught_subjects = Subject.objects.filter(teacher=request.user).select_related(
        'course', 'class_assigned', 'class_assigned__department'
    )
    
    # Get unique classes
    classes = {}
    for subject in taught_subjects:
        class_id = subject.class_assigned.id
        if class_id not in classes:
            classes[class_id] = {
                'class_obj': subject.class_assigned,
                'subjects': [],
                'student_count': Student.objects.filter(
                    student_class=subject.class_assigned,
                    is_active=True
                ).count()
            }
        classes[class_id]['subjects'].append(subject)
    
    context = {
        'teacher': teacher,
        'classes': classes.values(),
    }
    
    return render(request, 'teachers/classes.html', context)
