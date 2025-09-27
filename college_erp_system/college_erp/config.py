"""
Configuration constants for College ERP System
All hardcoded values should be defined here
"""
import os

# Academic Configuration
class AcademicConfig:
    # Attendance thresholds
    MINIMUM_ATTENDANCE_PERCENTAGE = float(os.getenv('MINIMUM_ATTENDANCE_PERCENTAGE', '75'))
    EXCELLENT_ATTENDANCE_PERCENTAGE = float(os.getenv('EXCELLENT_ATTENDANCE_PERCENTAGE', '85'))
    
    # Grade thresholds
    PASSING_GRADE_PERCENTAGE = float(os.getenv('PASSING_GRADE_PERCENTAGE', '60'))
    DISTINCTION_GRADE_PERCENTAGE = float(os.getenv('DISTINCTION_GRADE_PERCENTAGE', '85'))
    
    # Academic year
    DEFAULT_ACADEMIC_YEAR = os.getenv('DEFAULT_ACADEMIC_YEAR', '2024-2025')
    
    # Semester options
    SEMESTER_CHOICES = [
        (1, '1st Semester'),
        (2, '2nd Semester'),
        (3, '3rd Semester'),
        (4, '4th Semester'),
        (5, '5th Semester'),
        (6, '6th Semester'),
        (7, '7th Semester'),
        (8, '8th Semester'),
    ]

# Institution Configuration
class InstitutionConfig:
    NAME = os.getenv('INSTITUTION_NAME', 'College Name')
    SHORT_NAME = os.getenv('INSTITUTION_SHORT_NAME', 'College')
    ADDRESS = os.getenv('INSTITUTION_ADDRESS', '')
    PHONE = os.getenv('INSTITUTION_PHONE', '')
    EMAIL = os.getenv('INSTITUTION_EMAIL', '')
    WEBSITE = os.getenv('INSTITUTION_WEBSITE', '')

# Application Configuration
class AppConfig:
    # Pagination
    PAGINATION_PER_PAGE = int(os.getenv('PAGINATION_PER_PAGE', '10'))
    
    # File upload limits
    MAX_UPLOAD_SIZE = int(os.getenv('MAX_UPLOAD_SIZE', '5242880'))  # 5MB
    
    # Session settings
    SESSION_TIMEOUT = int(os.getenv('SESSION_TIMEOUT', '3600'))  # 1 hour
    
    # Default user permissions
    DEFAULT_STUDENT_PERMISSIONS = [
        'view_own_profile',
        'view_own_attendance',
        'view_own_results',
        'view_own_fees',
    ]
    
    DEFAULT_TEACHER_PERMISSIONS = [
        'view_own_profile',
        'mark_attendance',
        'view_class_students',
        'enter_grades',
    ]

# Time Configuration
class TimeConfig:
    # Standard class duration in minutes
    CLASS_DURATION_MINUTES = int(os.getenv('CLASS_DURATION_MINUTES', '60'))
    
    # Break durations
    SHORT_BREAK_MINUTES = int(os.getenv('SHORT_BREAK_MINUTES', '15'))
    LUNCH_BREAK_MINUTES = int(os.getenv('LUNCH_BREAK_MINUTES', '60'))
    
    # Standard time slots
    STANDARD_TIME_SLOTS = [
        ('08:00:00', '09:00:00', '8:00 AM - 9:00 AM'),
        ('09:00:00', '10:00:00', '9:00 AM - 10:00 AM'),
        ('10:00:00', '11:00:00', '10:00 AM - 11:00 AM'),
        ('11:00:00', '12:00:00', '11:00 AM - 12:00 PM'),
        ('12:00:00', '13:00:00', '12:00 PM - 1:00 PM'),
        ('13:00:00', '14:00:00', '1:00 PM - 2:00 PM'),
        ('14:00:00', '15:00:00', '2:00 PM - 3:00 PM'),
        ('15:00:00', '16:00:00', '3:00 PM - 4:00 PM'),
        ('16:00:00', '17:00:00', '4:00 PM - 5:00 PM'),
    ]
    
    WEEKDAYS = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'), 
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday')
    ]

# Fee Configuration
class FeeConfig:
    # Fee types
    FEE_TYPES = [
        ('tuition', 'Tuition Fee'),
        ('library', 'Library Fee'),
        ('laboratory', 'Laboratory Fee'),
        ('examination', 'Examination Fee'),
        ('sports', 'Sports Fee'),
        ('miscellaneous', 'Miscellaneous Fee'),
    ]
    
    # Payment status
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]

# User Configuration
class UserConfig:
    # User types
    USER_TYPES = [
        ('admin', 'Administrator'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]
    
    # Default password requirements
    MIN_PASSWORD_LENGTH = int(os.getenv('MIN_PASSWORD_LENGTH', '8'))
    
    # Profile picture settings
    ALLOWED_IMAGE_FORMATS = ['jpg', 'jpeg', 'png', 'gif']
    MAX_IMAGE_SIZE = int(os.getenv('MAX_IMAGE_SIZE', '2097152'))  # 2MB