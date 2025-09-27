from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from django.utils import timezone
from datetime import datetime, timedelta

from academics.models import (
    Timetable, Attendance, Exam, Result, Fee, Subject
)
from .models import Student, Notification
from college_erp.config import AcademicConfig, TimeConfig

@login_required
def dashboard(request):
    """Student dashboard with overview"""
    if not request.user.is_student:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('accounts:login')
    
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        messages.error(request, "Student profile not found. Please contact administrator.")
        return redirect('accounts:login')
    
    # Get attendance data only if records exist
    total_attendance = Attendance.objects.filter(student=request.user).count()
    present_attendance = Attendance.objects.filter(student=request.user, is_present=True).count()
    attendance_percentage = (present_attendance / total_attendance * 100) if total_attendance > 0 else None
    
    # Get upcoming exams only for student's class
    upcoming_exams = []
    if student.student_class:
        upcoming_exams = Exam.objects.filter(
            subject__class_assigned=student.student_class,
            date__gte=timezone.now()
        ).order_by('date')[:5]
    
    # Get pending fees
    pending_fees = Fee.objects.filter(
        student=request.user,
        payment_status__in=['pending', 'overdue']
    ).order_by('due_date')
    
    # Get recent notifications
    recent_notifications = Notification.objects.filter(
        Q(target_audience='all') |
        Q(target_audience='class', target_class=student.student_class) |
        Q(target_audience='department', target_department=student.department) |
        Q(target_audience='individual', target_student=student)
    ).order_by('-created_at')[:5]
    
    context = {
        'student': student,
        'attendance_percentage': round(attendance_percentage, 1) if attendance_percentage is not None else None,
        'has_attendance_data': total_attendance > 0,
        'total_attendance_records': total_attendance,
        'present_attendance': present_attendance,
        'upcoming_exams': upcoming_exams,
        'has_exam_data': upcoming_exams.exists() if upcoming_exams else False,
        'pending_fees': pending_fees,
        'recent_notifications': recent_notifications,
    }
    return render(request, 'students/dashboard.html', context)

@login_required
def timetable(request):
    """Display student's class timetable"""
    if not request.user.is_student:
        messages.error(request, "Access denied.")
        return redirect('accounts:login')
    
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        messages.error(request, "Student profile not found. Please contact administrator.")
        return redirect('accounts:login')
    
    if not student.student_class:
        messages.warning(request, "You are not assigned to any class. Please contact administrator.")
        return render(request, 'students/timetable.html', {'student': student})
    
    # Get timetable entries for student's class
    timetable_entries = Timetable.objects.filter(
        class_assigned=student.student_class
    ).select_related(
        'subject__course', 
        'time_slot',
        'subject__teacher'
    ).order_by('time_slot__day', 'time_slot__start_time')
    
    # Define standard time slots and days using config
    standard_times = [slot[:2] for slot in TimeConfig.STANDARD_TIME_SLOTS]
    days = TimeConfig.WEEKDAYS
    
    # Organize timetable by day
    organized_timetable = {}
    active_days = 0
    for day_key, day_name in days:
        day_classes = timetable_entries.filter(time_slot__day=day_key)
        organized_timetable[day_key] = day_classes
        if day_classes.exists():
            active_days += 1
    
    context = {
        'student': student,
        'timetable_entries': timetable_entries,
        'organized_timetable': organized_timetable,
        'standard_times': standard_times,
        'days': days,
        'active_days': active_days,
    }
    return render(request, 'students/timetable.html', context)

@login_required
def attendance(request):
    """Display student's attendance records"""
    if not request.user.is_student:
        messages.error(request, "Access denied.")
        return redirect('accounts:login')
    
    student = request.user.student_profile
    
    # Get attendance records for current semester
    attendance_records = Attendance.objects.filter(
        student=request.user
    ).select_related('subject__course').order_by('-date')
    
    # Calculate attendance percentage by subject only if student has a class
    subjects = []
    subject_attendance = {}
    
    if student.student_class:
        subjects = Subject.objects.filter(class_assigned=student.student_class)
        
        for subject in subjects:
            total = attendance_records.filter(subject=subject).count()
            present = attendance_records.filter(subject=subject, is_present=True).count()
            percentage = (present / total * 100) if total > 0 else None
            subject_attendance[subject] = {
                'total': total,
                'present': present,
                'absent': total - present,
                'percentage': round(percentage, 1) if percentage is not None else None,
                'has_data': total > 0
            }
    
    # Calculate overall attendance
    total_attendance = attendance_records.count()
    present_total = attendance_records.filter(is_present=True).count()
    overall_percentage = (present_total / total_attendance * 100) if total_attendance > 0 else None
    
    context = {
        'student': student,
        'attendance_records': attendance_records,
        'subject_attendance': subject_attendance,
        'has_attendance_data': total_attendance > 0,
        'overall_attendance_percentage': round(overall_percentage, 1) if overall_percentage is not None else None,
        'total_classes_held': total_attendance,
        'has_class_assigned': student.student_class is not None,
    }
    return render(request, 'students/attendance.html', context)

@login_required
def exams(request):
    """Display upcoming and past exams"""
    if not request.user.is_student:
        messages.error(request, "Access denied.")
        return redirect('accounts:login')
    
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        messages.error(request, "Student profile not found. Please contact administrator.")
        return redirect('accounts:login')
    
    upcoming_exams = []
    past_exams = []
    
    # Only get exams if student is assigned to a class
    if student.student_class:
        upcoming_exams = Exam.objects.filter(
            subject__class_assigned=student.student_class,
            date__gte=timezone.now()
        ).select_related('subject__course').order_by('date')
        
        past_exams = Exam.objects.filter(
            subject__class_assigned=student.student_class,
            date__lt=timezone.now()
        ).select_related('subject__course').order_by('-date')
    
    context = {
        'student': student,
        'upcoming_exams': upcoming_exams,
        'past_exams': past_exams,
        'has_upcoming_exams': upcoming_exams.exists() if upcoming_exams else False,
        'has_past_exams': past_exams.exists() if past_exams else False,
        'has_class_assigned': student.student_class is not None,
    }
    return render(request, 'students/exams.html', context)

@login_required
def results(request):
    """Display exam results"""
    if not request.user.is_student:
        messages.error(request, "Access denied.")
        return redirect('accounts:login')
    
    student = request.user.student_profile
    
    results = Result.objects.filter(
        student=request.user,
        is_published=True
    ).select_related('exam__subject__course').order_by('-exam__date')
    
    # Calculate overall performance and statistics
    total_marks = sum([r.exam.total_marks for r in results])
    obtained_marks = sum([r.marks_obtained or 0 for r in results])
    overall_percentage = (obtained_marks / total_marks * 100) if total_marks > 0 else 0
    
    # Count passed exams using configuration
    passing_threshold = AcademicConfig.PASSING_GRADE_PERCENTAGE / 100
    passed_count = sum(1 for r in results if (r.marks_obtained or 0) >= (r.exam.total_marks * passing_threshold))
    
    # Count distinctions using configuration
    distinction_threshold = AcademicConfig.DISTINCTION_GRADE_PERCENTAGE / 100
    distinctions_count = sum(1 for r in results if (r.marks_obtained or 0) >= (r.exam.total_marks * distinction_threshold))
    
    # Add percentage calculation to each result
    results_with_percentage = []
    for result in results:
        percentage = ((result.marks_obtained or 0) / result.exam.total_marks * 100) if result.exam.total_marks > 0 else 0
        # Add percentage as an attribute to the result object
        result.percentage = round(percentage, 1)
        results_with_percentage.append(result)
    
    context = {
        'student': student,
        'results': results_with_percentage,
        'overall_percentage': round(overall_percentage, 1),
        'passed_count': passed_count,
        'distinctions_count': distinctions_count,
        'total_obtained': int(obtained_marks),
        'total_possible': int(total_marks),
    }
    return render(request, 'students/results.html', context)

@login_required
def fees(request):
    """Display fee details and payment status"""
    if not request.user.is_student:
        messages.error(request, "Access denied.")
        return redirect('accounts:login')
    
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        messages.error(request, "Student profile not found. Please contact administrator.")
        return redirect('accounts:login')
    
    all_fees = Fee.objects.filter(
        student=request.user
    ).order_by('-created_at')
    
    pending_fees = all_fees.filter(payment_status__in=['pending', 'overdue'])
    paid_fees = all_fees.filter(payment_status='paid')
    
    # Calculate totals
    total_pending = sum([fee.amount for fee in pending_fees])
    total_paid = sum([fee.amount for fee in paid_fees])
    
    context = {
        'student': student,
        'all_fees': all_fees,
        'pending_fees': pending_fees,
        'paid_fees': paid_fees,
        'total_pending': total_pending,
        'total_paid': total_paid,
    }
    return render(request, 'students/fees.html', context)

@login_required
def notifications(request):
    """Display notifications for student"""
    if not request.user.is_student:
        messages.error(request, "Access denied.")
        return redirect('accounts:login')
    
    student = request.user.student_profile
    
    notifications = Notification.objects.filter(
        Q(target_audience='all') |
        Q(target_audience='class', target_class=student.student_class) |
        Q(target_audience='department', target_department=student.department) |
        Q(target_audience='individual', target_student=student)
    ).order_by('-created_at')
    
    context = {
        'student': student,
        'notifications': notifications,
    }
    return render(request, 'students/notifications.html', context)
