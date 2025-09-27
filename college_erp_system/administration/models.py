from django.db import models
from accounts.models import User
from django.utils import timezone

class Notification(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    RECIPIENT_TYPE_CHOICES = [
        ('all', 'All Users'),
        ('students', 'All Students'),
        ('teachers', 'All Teachers'),
        ('admins', 'All Administrators'),
        ('specific', 'Specific Users'),
    ]
    
    title = models.CharField(max_length=200)
    message = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    recipient_type = models.CharField(max_length=20, choices=RECIPIENT_TYPE_CHOICES, default='all')
    specific_recipients = models.ManyToManyField(User, related_name='received_notifications', blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.title} - {self.get_recipient_type_display()}"
    
    @property
    def is_expired(self):
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False
    
    def get_recipients(self):
        """Get all recipients based on recipient_type"""
        if self.recipient_type == 'all':
            return User.objects.filter(is_active=True)
        elif self.recipient_type == 'students':
            return User.objects.filter(user_type='student', is_active=True)
        elif self.recipient_type == 'teachers':
            return User.objects.filter(user_type='teacher', is_active=True)
        elif self.recipient_type == 'admins':
            return User.objects.filter(user_type='admin', is_active=True)
        elif self.recipient_type == 'specific':
            return self.specific_recipients.filter(is_active=True)
        return User.objects.none()

class NotificationRead(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='read_status')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['notification', 'user']
        
    def __str__(self):
        return f"{self.user.username} read {self.notification.title}"
