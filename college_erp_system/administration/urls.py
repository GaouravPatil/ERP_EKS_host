from django.urls import path
from . import views

app_name = 'administration'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('users/', views.users, name='users'),
    path('users/<int:user_id>/', views.user_profile, name='user_profile'),
    path('users/<int:user_id>/change-password/', views.change_user_password, name='change_user_password'),
    path('users/<int:user_id>/reset-password/', views.reset_user_password, name='reset_user_password'),
    path('users/<int:user_id>/toggle-status/', views.toggle_user_status, name='toggle_user_status'),
    path('reports/', views.reports, name='reports'),
    path('hods/', views.hods, name='hods'),
    
    # Notification management URLs
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/send/', views.send_notification, name='send_notification'),
    path('notifications/<int:notification_id>/', views.notification_detail, name='notification_detail'),
    path('notifications/<int:notification_id>/toggle/', views.toggle_notification_status, name='toggle_notification_status'),
    path('notifications/<int:notification_id>/delete/', views.delete_notification, name='delete_notification'),
    
    # AJAX endpoints
    path('api/users-by-type/', views.get_users_by_type, name='get_users_by_type'),
]
