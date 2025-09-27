#!/usr/bin/env python
"""
Teacher Dashboard Test Script
Tests the newly implemented teacher dashboard features
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_erp.settings')
sys.path.append('/home/rival/Desktop/python_project/college_erp_system')

django.setup()

from django.contrib.auth import get_user_model
from teachers.models import Teacher
from academics.models import Subject, Class, Timetable, Department

User = get_user_model()

def test_teacher_system():
    print("🎓 Testing Teacher Dashboard System...")
    print("=" * 50)
    
    # Check if we have teachers
    try:
        teachers = Teacher.objects.all()
        print(f"✅ Found {teachers.count()} teachers in the system")
        
        for teacher in teachers[:3]:  # Show first 3 teachers
            print(f"   - {teacher.user.get_full_name() or teacher.user.username} (ID: {teacher.employee_id})")
            print(f"     Department: {teacher.department.name}")
            print(f"     Designation: {teacher.designation}")
    
    except Exception as e:
        print(f"❌ Error getting teachers: {e}")
        return False
    
    # Check subjects and classes
    print("\n🔍 Checking academic structure...")
    
    try:
        subjects = Subject.objects.all()
        classes = Class.objects.all()
        departments = Department.objects.all()
        
        print(f"✅ Found {subjects.count()} subjects")
        print(f"✅ Found {classes.count()} classes")
        print(f"✅ Found {departments.count()} departments")
        
        # Check if we have teachers assigned to subjects
        taught_subjects = Subject.objects.filter(teacher__isnull=False)
        print(f"✅ Found {taught_subjects.count()} subjects with assigned teachers")
        
    except Exception as e:
        print(f"❌ Error checking academic structure: {e}")
    
    # Check timetable
    print("\n📅 Checking timetable structure...")
    try:
        timetables = Timetable.objects.all()
        print(f"✅ Found {timetables.count()} timetable entries")
        
        if timetables.count() > 0:
            sample_timetable = timetables.first()
            print(f"   Sample: {sample_timetable.subject.course.name} - {sample_timetable.time_slot}")
        
    except Exception as e:
        print(f"❌ Error checking timetable: {e}")
    
    print("\n🎉 Teacher system test completed!")
    return True

if __name__ == "__main__":
    test_teacher_system()