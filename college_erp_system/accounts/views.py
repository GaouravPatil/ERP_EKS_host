from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from .models import User
from administration.models import Notification, NotificationRead
import json

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Redirect based on user type
            if user.is_admin:
                return redirect('administration:dashboard')
            elif user.is_teacher:
                return redirect('teachers:dashboard')
            elif user.is_student:
                return redirect('students:dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:login')

@login_required
def profile(request):
    """User profile view with editing capabilities"""
    user = request.user
    
    if request.method == 'POST':
        try:
            # Update basic information
            user.first_name = request.POST.get('first_name', '').strip()
            user.last_name = request.POST.get('last_name', '').strip()
            user.email = request.POST.get('email', '').strip()
            user.phone_number = request.POST.get('phone_number', '').strip()
            user.address = request.POST.get('address', '').strip()
            user.date_of_birth = request.POST.get('date_of_birth') or None
            
            # Handle profile picture upload
            if 'profile_picture' in request.FILES:
                user.profile_picture = request.FILES['profile_picture']
            
            user.save()
            
            messages.success(request, 'Your profile has been updated successfully!')
            return JsonResponse({
                'success': True, 
                'message': 'Profile updated successfully!',
                'redirect': reverse('accounts:profile')
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'message': f'Error updating profile: {str(e)}'
            })
    
    # Calculate profile completion
    profile_fields = [
        user.first_name, user.last_name, user.email, 
        user.phone_number, user.address, user.date_of_birth, user.profile_picture
    ]
    completed_fields = len([field for field in profile_fields if field])
    profile_completion = int((completed_fields / len(profile_fields)) * 100)
    
    context = {
        'user': user,
        'profile_completion': profile_completion,
        'completed_fields': completed_fields,
        'total_fields': len(profile_fields),
    }
    
    return render(request, 'accounts/profile.html', context)

@login_required
def change_password(request):
    """Change user password"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'accounts/change_password.html', {'form': form})

@login_required
def dashboard_redirect(request):
    """Redirect users to their appropriate dashboard based on role"""
    user = request.user
    if user.is_admin:
        return redirect('administration:dashboard')
    elif user.is_teacher:
        return redirect('teachers:dashboard')
    elif user.is_student:
        return redirect('students:dashboard')
    else:
        return redirect('accounts:login')

@login_required
def notifications(request):
    """Display notifications for the current user"""
    user = request.user
    current_time = timezone.now()
    
    # Get notifications for this user based on recipient type
    user_notifications = Notification.objects.filter(
        Q(recipient_type='all') |
        Q(recipient_type=user.user_type) |
        Q(specific_recipients=user),
        is_active=True,
        created_at__lte=current_time
    ).filter(
        Q(expires_at__isnull=True) | Q(expires_at__gt=current_time)
    ).distinct().order_by('-created_at')
    
    # Filter by status if specified
    status_filter = request.GET.get('status', 'all')
    read_notifications = NotificationRead.objects.filter(user=user).values_list('notification_id', flat=True)
    
    if status_filter == 'read':
        user_notifications = user_notifications.filter(id__in=read_notifications)
    elif status_filter == 'unread':
        user_notifications = user_notifications.exclude(id__in=read_notifications)
    
    # Pagination
    paginator = Paginator(user_notifications, 10)
    page_number = request.GET.get('page')
    notifications_page = paginator.get_page(page_number)
    
    # Add read status to each notification
    notifications_with_status = []
    for notification in notifications_page:
        is_read = notification.id in read_notifications
        notifications_with_status.append({
            'notification': notification,
            'is_read': is_read,
            'read_record': NotificationRead.objects.filter(
                notification=notification, user=user
            ).first() if is_read else None
        })
    
    # Get notification counts
    total_notifications = user_notifications.count()
    read_count = user_notifications.filter(id__in=read_notifications).count()
    unread_count = total_notifications - read_count
    
    context = {
        'notifications': notifications_with_status,
        'page_obj': notifications_page,
        'total_notifications': total_notifications,
        'read_count': read_count,
        'unread_count': unread_count,
        'status_filter': status_filter,
    }
    
    return render(request, 'accounts/notifications.html', context)

@login_required
def notification_detail(request, notification_id):
    """View a specific notification and mark as read"""
    user = request.user
    current_time = timezone.now()
    
    # Get the notification ensuring user has access to it
    notification = get_object_or_404(
        Notification.objects.filter(
            Q(recipient_type='all') |
            Q(recipient_type=user.user_type) |
            Q(specific_recipients=user),
            is_active=True
        ).filter(
            Q(expires_at__isnull=True) | Q(expires_at__gt=current_time)
        ),
        id=notification_id
    )
    
    # Mark as read if not already read
    read_record, created = NotificationRead.objects.get_or_create(
        notification=notification,
        user=user
    )
    
    context = {
        'notification': notification,
        'read_record': read_record,
        'is_new': created,
    }
    
    return render(request, 'accounts/notification_detail.html', context)

@login_required
def mark_notification_read(request, notification_id):
    """Mark a notification as read via AJAX"""
    if request.method == 'POST':
        user = request.user
        try:
            notification = get_object_or_404(Notification, id=notification_id)
            read_record, created = NotificationRead.objects.get_or_create(
                notification=notification,
                user=user
            )
            return JsonResponse({
                'success': True,
                'message': 'Notification marked as read',
                'was_new': created
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@login_required
def get_unread_count(request):
    """Get count of unread notifications for current user"""
    user = request.user
    current_time = timezone.now()
    
    # Get all notifications for this user
    user_notifications = Notification.objects.filter(
        Q(recipient_type='all') |
        Q(recipient_type=user.user_type) |
        Q(specific_recipients=user),
        is_active=True,
        created_at__lte=current_time
    ).filter(
        Q(expires_at__isnull=True) | Q(expires_at__gt=current_time)
    ).distinct()
    
    # Get read notifications
    read_notifications = NotificationRead.objects.filter(user=user).values_list('notification_id', flat=True)
    
    # Count unread
    unread_count = user_notifications.exclude(id__in=read_notifications).count()
    
    return JsonResponse({'unread_count': unread_count})