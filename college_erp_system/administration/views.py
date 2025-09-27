from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Q, Sum, Avg
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.core.paginator import Paginator
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.forms import SetPasswordForm
from datetime import datetime, timedelta
import json

from academics.models import Department, Course, Class, Subject, Attendance, Exam, Result, Fee
from students.models import Student, Notification as StudentNotification
from teachers.models import Teacher
from .models import Notification, NotificationRead

User = get_user_model()

def is_admin(user):
    return user.is_authenticated and user.is_admin

@login_required
@user_passes_test(is_admin)
def dashboard(request):
    """Administration dashboard with statistics"""
    # Get basic counts
    total_students = Student.objects.filter(is_active=True).count()
    total_teachers = Teacher.objects.filter(is_active=True).count()
    total_departments = Department.objects.count()
    total_courses = Course.objects.count()
    total_classes = Class.objects.count()
    
    # Get recent statistics
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    
    # Recent attendance percentage
    recent_attendance = Attendance.objects.filter(date__gte=week_ago)
    total_attendance_records = recent_attendance.count()
    present_records = recent_attendance.filter(is_present=True).count()
    attendance_percentage = (present_records / total_attendance_records * 100) if total_attendance_records > 0 else 0
    
    # Upcoming exams
    upcoming_exams = Exam.objects.filter(
        date__gte=timezone.now(),
        date__lte=timezone.now() + timedelta(days=7)
    ).count()
    
    # Pending fees
    pending_fees_count = Fee.objects.filter(
        payment_status__in=['pending', 'overdue']
    ).count()
    
    pending_fees_amount = Fee.objects.filter(
        payment_status__in=['pending', 'overdue']
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    # Recent notifications
    recent_notifications = Notification.objects.filter(
        created_at__gte=week_ago
    ).order_by('-created_at')[:5]
    
    # Department-wise student count with HOD info
    department_stats = []
    for dept in Department.objects.annotate(
        student_count=Count('student', filter=Q(student__is_active=True))
    ).order_by('-student_count'):
        percentage = (dept.student_count / total_students * 100) if total_students > 0 else 0
        department_stats.append({
            'dept': dept,
            'student_count': dept.student_count,
            'percentage': round(percentage, 1)
        })
    
    # HOD Statistics
    departments_with_hods = Department.objects.filter(head__isnull=False).count()
    hod_coverage_percentage = (departments_with_hods / total_departments * 100) if total_departments > 0 else 0
    
    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_departments': total_departments,
        'total_courses': total_courses,
        'total_classes': total_classes,
        'attendance_percentage': round(attendance_percentage, 1),
        'upcoming_exams': upcoming_exams,
        'pending_fees_count': pending_fees_count,
        'pending_fees_amount': pending_fees_amount,
        'recent_notifications': recent_notifications,
        'department_stats': department_stats,
        'departments_with_hods': departments_with_hods,
        'hod_coverage_percentage': round(hod_coverage_percentage, 1),
    }
    return render(request, 'administration/dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def users(request):
    """User management page"""
    user_type = request.GET.get('type', 'all')
    search_query = request.GET.get('search', '')
    
    users_queryset = User.objects.all().order_by('-date_joined')
    
    if user_type != 'all':
        users_queryset = users_queryset.filter(user_type=user_type)
    
    if search_query:
        users_queryset = users_queryset.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(users_queryset, 20)  # Show 20 users per page
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)
    
    # Count by user type
    user_counts = {
        'all': User.objects.count(),
        'student': User.objects.filter(user_type='student').count(),
        'teacher': User.objects.filter(user_type='teacher').count(),
        'admin': User.objects.filter(user_type='admin').count(),
    }
    
    context = {
        'users': users,
        'user_counts': user_counts,
        'current_type': user_type,
        'search_query': search_query,
    }
    return render(request, 'administration/users.html', context)

@login_required
@user_passes_test(is_admin)
def user_profile(request, user_id):
    """View and edit individual user profile"""
    target_user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        try:
            # Update user information
            target_user.first_name = request.POST.get('first_name', '').strip()
            target_user.last_name = request.POST.get('last_name', '').strip()
            target_user.email = request.POST.get('email', '').strip()
            target_user.phone_number = request.POST.get('phone_number', '').strip()
            target_user.address = request.POST.get('address', '').strip()
            target_user.date_of_birth = request.POST.get('date_of_birth') or None
            target_user.is_active = request.POST.get('is_active') == 'on'
            
            # Handle profile picture upload
            if 'profile_picture' in request.FILES:
                target_user.profile_picture = request.FILES['profile_picture']
            
            # Handle user type change
            new_user_type = request.POST.get('user_type')
            if new_user_type in ['student', 'teacher', 'admin']:
                target_user.user_type = new_user_type
            
            target_user.save()
            
            messages.success(request, f'Profile for {target_user.get_full_name()} updated successfully!')
            return redirect('administration:user_profile', user_id=user_id)
            
        except Exception as e:
            messages.error(request, f'Error updating profile: {str(e)}')
    
    # Calculate profile completion
    profile_fields = [
        target_user.first_name, target_user.last_name, target_user.email, 
        target_user.phone_number, target_user.address, target_user.date_of_birth, 
        target_user.profile_picture
    ]
    completed_fields = len([field for field in profile_fields if field])
    profile_completion = int((completed_fields / len(profile_fields)) * 100)
    
    # Get user's additional information based on type
    additional_info = None
    if target_user.user_type == 'student':
        try:
            additional_info = Student.objects.get(user=target_user)
        except Student.DoesNotExist:
            pass
    elif target_user.user_type == 'teacher':
        try:
            additional_info = Teacher.objects.get(user=target_user)
        except Teacher.DoesNotExist:
            pass
    
    context = {
        'target_user': target_user,
        'profile_completion': profile_completion,
        'completed_fields': completed_fields,
        'total_fields': len(profile_fields),
        'additional_info': additional_info,
    }
    
    return render(request, 'administration/user_profile.html', context)

@login_required
@user_passes_test(is_admin)
def change_user_password(request, user_id):
    """Change password for any user"""
    target_user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = SetPasswordForm(target_user, request.POST)
        if form.is_valid():
            form.save()
            # Don't update session auth hash for other users
            messages.success(
                request, 
                f'Password successfully changed for {target_user.get_full_name()}!'
            )
            return redirect('administration:user_profile', user_id=user_id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SetPasswordForm(target_user)
    
    context = {
        'form': form,
        'target_user': target_user,
    }
    return render(request, 'administration/change_user_password.html', context)

@login_required
@user_passes_test(is_admin)
def reset_user_password(request, user_id):
    """Reset user password to default"""
    if request.method == 'POST':
        target_user = get_object_or_404(User, id=user_id)
        
        # Set default password based on user type and username
        if target_user.user_type == 'student':
            default_password = f"{target_user.username}@123"
        elif target_user.user_type == 'teacher':
            default_password = f"{target_user.username}@123"
        else:
            default_password = "admin@123"
        
        target_user.set_password(default_password)
        target_user.save()
        
        messages.success(
            request,
            f'Password reset for {target_user.get_full_name()}! New password: {default_password}'
        )
        return redirect('administration:user_profile', user_id=user_id)
    
    return redirect('administration:users')

@login_required
@user_passes_test(is_admin)
def toggle_user_status(request, user_id):
    """Toggle user active/inactive status"""
    if request.method == 'POST':
        target_user = get_object_or_404(User, id=user_id)
        target_user.is_active = not target_user.is_active
        target_user.save()
        
        status = 'activated' if target_user.is_active else 'deactivated'
        messages.success(request, f'User {target_user.get_full_name()} has been {status}.')
    
    return redirect('administration:users')

@login_required
@user_passes_test(is_admin)
def reports(request):
    """Generate and display various reports"""
    report_type = request.GET.get('report', 'overview')
    
    context = {'report_type': report_type}
    
    if report_type == 'attendance':
        # Attendance report
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        
        attendance_query = Attendance.objects.all()
        
        if date_from:
            attendance_query = attendance_query.filter(date__gte=date_from)
        if date_to:
            attendance_query = attendance_query.filter(date__lte=date_to)
        
        # Overall attendance statistics
        total_records = attendance_query.count()
        present_records = attendance_query.filter(is_present=True).count()
        overall_percentage = (present_records / total_records * 100) if total_records > 0 else 0
        
        # Class-wise attendance
        class_attendance = {}
        for class_obj in Class.objects.all():
            class_records = attendance_query.filter(
                subject__class_assigned=class_obj
            )
            class_total = class_records.count()
            class_present = class_records.filter(is_present=True).count()
            class_percentage = (class_present / class_total * 100) if class_total > 0 else 0
            
            class_attendance[class_obj] = {
                'total': class_total,
                'present': class_present,
                'percentage': round(class_percentage, 1)
            }
        
        context.update({
            'overall_percentage': round(overall_percentage, 1),
            'total_records': total_records,
            'present_records': present_records,
            'class_attendance': class_attendance,
            'date_from': date_from,
            'date_to': date_to,
        })
        
    elif report_type == 'financial':
        # Financial report
        total_fees = Fee.objects.aggregate(
            total_amount=Sum('amount'),
            paid_amount=Sum('amount', filter=Q(payment_status='paid')),
            pending_amount=Sum('amount', filter=Q(payment_status__in=['pending', 'overdue']))
        )
        
        # Fee type breakdown
        fee_breakdown = Fee.objects.values('fee_type').annotate(
            total=Sum('amount'),
            paid=Sum('amount', filter=Q(payment_status='paid')),
            pending=Sum('amount', filter=Q(payment_status__in=['pending', 'overdue']))
        ).order_by('-total')
        
        context.update({
            'total_fees': total_fees,
            'fee_breakdown': fee_breakdown,
        })
    
    elif report_type == 'academic':
        # Academic performance report
        subjects_with_results = Subject.objects.annotate(
            total_students=Count('class_assigned__students', filter=Q(class_assigned__students__is_active=True)),
            total_results=Count('exam__result'),
            avg_marks=Avg('exam__result__marks_obtained')
        ).filter(total_results__gt=0)
        
        context.update({
            'subjects_with_results': subjects_with_results,
        })
    
    return render(request, 'administration/reports.html', context)


@login_required
@user_passes_test(is_admin)
def hods(request):
    """Display Head of Departments information"""
    departments_with_hods = Department.objects.filter(head__isnull=False).select_related('head', 'head__teacher_profile')
    departments_without_hods = Department.objects.filter(head__isnull=True)
    
    # Prepare HOD data
    hod_data = []
    for dept in departments_with_hods:
        hod_info = {
            'department': dept,
            'hod_user': dept.head,
            'teacher_profile': getattr(dept.head, 'teacher_profile', None),
            'total_teachers': Teacher.objects.filter(department=dept, is_active=True).count(),
            'total_students': Student.objects.filter(department=dept, is_active=True).count(),
            'total_courses': Course.objects.filter(department=dept).count(),
        }
        hod_data.append(hod_info)
    
    # Sort by department name
    hod_data.sort(key=lambda x: x['department'].name)
    
    context = {
        'hod_data': hod_data,
        'departments_without_hods': departments_without_hods,
        'total_departments': Department.objects.count(),
        'departments_with_hods_count': len(hod_data),
    }
    
    return render(request, 'administration/hods.html', context)

@login_required
@user_passes_test(is_admin)
def notifications(request):
    """Display all sent notifications"""
    notifications = Notification.objects.all().order_by('-created_at')
    
    # Filter by status if specified
    status_filter = request.GET.get('status', 'all')
    if status_filter == 'active':
        notifications = notifications.filter(is_active=True)
    elif status_filter == 'expired':
        notifications = notifications.filter(expires_at__lt=timezone.now())
    
    # Pagination
    paginator = Paginator(notifications, 10)
    page_number = request.GET.get('page')
    notifications = paginator.get_page(page_number)
    
    # Get notification statistics
    stats = {
        'total': Notification.objects.count(),
        'active': Notification.objects.filter(is_active=True).count(),
        'expired': Notification.objects.filter(expires_at__lt=timezone.now()).count(),
        'this_week': Notification.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=7)
        ).count(),
    }
    
    context = {
        'notifications': notifications,
        'stats': stats,
        'status_filter': status_filter,
    }
    return render(request, 'administration/notifications.html', context)

@login_required
@user_passes_test(is_admin)
def send_notification(request):
    """Send notification to users"""
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            message = request.POST.get('message')
            recipient_type = request.POST.get('recipient_type')
            priority = request.POST.get('priority', 'medium')
            expires_at = request.POST.get('expires_at')
            specific_recipients = request.POST.getlist('specific_recipients')
            
            # Create notification
            notification = Notification.objects.create(
                title=title,
                message=message,
                sender=request.user,
                recipient_type=recipient_type,
                priority=priority,
                expires_at=expires_at if expires_at else None,
            )
            
            # Add specific recipients if selected
            if recipient_type == 'specific' and specific_recipients:
                notification.specific_recipients.set(specific_recipients)
            
            # Count recipients
            recipient_count = notification.get_recipients().count()
            
            messages.success(
                request, 
                f'Notification "{title}" sent successfully to {recipient_count} recipient(s)!'
            )
            return redirect('administration:notifications')
            
        except Exception as e:
            messages.error(request, f'Error sending notification: {str(e)}')
    
    # Get all users for specific recipient selection
    all_users = User.objects.filter(is_active=True).order_by('user_type', 'first_name', 'last_name')
    
    # Group users by type
    users_by_type = {
        'students': all_users.filter(user_type='student'),
        'teachers': all_users.filter(user_type='teacher'),
        'admins': all_users.filter(user_type='admin'),
    }
    
    context = {
        'users_by_type': users_by_type,
        'all_users': all_users,
    }
    return render(request, 'administration/send_notification.html', context)

@login_required
@user_passes_test(is_admin)
def notification_detail(request, notification_id):
    """View notification details and read status"""
    notification = get_object_or_404(Notification, id=notification_id)
    
    # Get read status
    read_status = NotificationRead.objects.filter(
        notification=notification
    ).select_related('user').order_by('-read_at')
    
    # Get recipients and their read status
    recipients = notification.get_recipients()
    recipient_data = []
    
    for recipient in recipients:
        read_record = read_status.filter(user=recipient).first()
        recipient_data.append({
            'user': recipient,
            'read_at': read_record.read_at if read_record else None,
            'is_read': read_record is not None,
        })
    
    # Statistics
    total_recipients = len(recipient_data)
    read_count = len([r for r in recipient_data if r['is_read']])
    unread_count = total_recipients - read_count
    read_percentage = (read_count / total_recipients * 100) if total_recipients > 0 else 0
    
    context = {
        'notification': notification,
        'recipient_data': recipient_data,
        'total_recipients': total_recipients,
        'read_count': read_count,
        'unread_count': unread_count,
        'read_percentage': round(read_percentage, 1),
    }
    return render(request, 'administration/notification_detail.html', context)

@login_required
@user_passes_test(is_admin)
def toggle_notification_status(request, notification_id):
    """Toggle notification active status"""
    if request.method == 'POST':
        notification = get_object_or_404(Notification, id=notification_id)
        notification.is_active = not notification.is_active
        notification.save()
        
        status = 'activated' if notification.is_active else 'deactivated'
        messages.success(request, f'Notification "{notification.title}" has been {status}.')
    
    return redirect('administration:notifications')

@login_required
@user_passes_test(is_admin)
def delete_notification(request, notification_id):
    """Delete notification"""
    if request.method == 'POST':
        notification = get_object_or_404(Notification, id=notification_id)
        title = notification.title
        notification.delete()
        messages.success(request, f'Notification "{title}" has been deleted.')
    
    return redirect('administration:notifications')

@login_required
def get_users_by_type(request):
    """AJAX endpoint to get users by type"""
    user_type = request.GET.get('type', '')
    users = []
    
    if user_type in ['student', 'teacher', 'admin']:
        users = User.objects.filter(
            user_type=user_type, 
            is_active=True
        ).values('id', 'username', 'first_name', 'last_name', 'email')
    
    return JsonResponse({'users': list(users)})
