from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from academics.models import Department, Course, Class
from students.models import Student
from teachers.models import Teacher
from datetime import date
from college_erp.config import AcademicConfig
import uuid

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample data for testing'

    def handle(self, *args, **options):
        # Create departments
        cs_dept = Department.objects.get_or_create(
            name='Computer Science',
            code='CS',
            description='Department of Computer Science'
        )[0]
        
        math_dept = Department.objects.get_or_create(
            name='Mathematics',
            code='MATH',
            description='Department of Mathematics'
        )[0]
        
        # Create sample admin user
        admin_username = f'admin_{uuid.uuid4().hex[:8]}'
        admin_user, created = User.objects.get_or_create(
            username=admin_username,
            defaults={
                'email': 'admin@college.edu',
                'first_name': 'System',
                'last_name': 'Administrator',
                'user_type': 'admin'
            }
        )
        if created:
            admin_user.set_password('change_this_password_123')
            admin_user.save()
        
        # Create sample teacher
        teacher_username = f'teacher_{uuid.uuid4().hex[:8]}'
        teacher_user, created = User.objects.get_or_create(
            username=teacher_username,
            defaults={
                'email': 'teacher@college.edu',
                'first_name': 'John',
                'last_name': 'Doe',
                'user_type': 'teacher'
            }
        )
        if created:
            teacher_user.set_password('change_this_password_123')
            teacher_user.save()
        
        teacher, _ = Teacher.objects.get_or_create(
            user=teacher_user,
            defaults={
                'employee_id': f'EMP{uuid.uuid4().hex[:6].upper()}',
                'department': cs_dept,
                'designation': 'Assistant Professor',
                'qualification': 'master',
                'specialization': 'Software Engineering',
                'experience_years': 5,
                'employment_type': 'permanent',
                'joining_date': date(2020, 1, 1)
            }
        )
        
        # Create sample student
        student_username = f'student_{uuid.uuid4().hex[:8]}'
        student_user, created = User.objects.get_or_create(
            username=student_username,
            defaults={
                'email': 'student@college.edu',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'user_type': 'student'
            }
        )
        if created:
            student_user.set_password('change_this_password_123')
            student_user.save()
        
        # Create a class using academic year from config
        student_class, _ = Class.objects.get_or_create(
            name='CS Semester 1 A',
            department=cs_dept,
            semester=1,
            section='A',
            academic_year=AcademicConfig.DEFAULT_ACADEMIC_YEAR,
            defaults={
                'class_teacher': teacher_user,
                'max_strength': 60
            }
        )
        
        # Create student profile
        student, _ = Student.objects.get_or_create(
            user=student_user,
            defaults={
                'roll_number': f'CS{uuid.uuid4().hex[:6].upper()}',
                'admission_number': f'ADM{date.today().year}{uuid.uuid4().hex[:6].upper()}',
                'student_class': student_class,
                'department': cs_dept,
                'admission_date': date(2024, 1, 1),
                'guardian_name': 'Guardian Name',
                'guardian_phone': '+1-XXX-XXX-XXXX',
                'guardian_email': 'guardian@example.com',
                'guardian_address': 'Guardian Address, City, State',
                'emergency_contact': '+1-XXX-XXX-XXXX',
                'blood_group': 'O+',
            }
        )
        
        # Create some courses
        Course.objects.get_or_create(
            name='Programming Fundamentals',
            code='CS101',
            department=cs_dept,
            semester=1,
            credits=4,
            description='Introduction to programming concepts'
        )
        
        Course.objects.get_or_create(
            name='Mathematics I',
            code='MATH101',
            department=math_dept,
            semester=1,
            credits=3,
            description='Basic mathematics for engineering'
        )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data!')
        )
        self.stdout.write('Demo Users (Please change passwords immediately):')
        self.stdout.write(f'  Admin: {admin_username}/change_this_password_123')
        self.stdout.write(f'  Teacher: {teacher_username}/change_this_password_123')
        self.stdout.write(f'  Student: {student_username}/change_this_password_123')
