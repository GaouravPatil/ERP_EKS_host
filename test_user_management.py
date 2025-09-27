#!/usr/bin/env python
"""
User Management System Test Script
Tests the newly implemented admin user management features
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_erp.settings')
sys.path.append('/home/rival/Desktop/python_project/college_erp_system')

django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm

User = get_user_model()

def test_user_management_system():
    print("🔍 Testing User Management System...")
    print("=" * 50)
    
    # Check if we can get users
    try:
        users = User.objects.all()
        print(f"✅ Found {users.count()} users in the system")
        
        for user in users[:5]:  # Show first 5 users
            print(f"   - {user.username} ({user.get_full_name() or 'No name'}) - {'Active' if user.is_active else 'Inactive'}")
    
    except Exception as e:
        print(f"❌ Error getting users: {e}")
        return False
    
    # Test default user creation/checking
    print("\n🔍 Checking for default users...")
    
    default_users = ['Student1', 'Teacher1', 'Admin1']
    for username in default_users:
        try:
            user = User.objects.get(username=username)
            print(f"✅ Default user '{username}' exists")
            
            # Check profile
            if hasattr(user, 'student_profile') and user.student_profile:
                print(f"   - Profile: Student (ID: {user.student_profile.student_id})")
            elif hasattr(user, 'teacher_profile') and user.teacher_profile:
                print(f"   - Profile: Teacher (ID: {user.teacher_profile.employee_id})")
            else:
                print(f"   - Profile: Admin/Staff user")
                
        except User.DoesNotExist:
            print(f"⚠️  Default user '{username}' not found")
    
    # Test password form functionality
    print("\n🔍 Testing password form functionality...")
    try:
        test_user = User.objects.first()
        if test_user:
            form = SetPasswordForm(test_user)
            print("✅ SetPasswordForm initialized successfully")
            print(f"   - Form fields: {list(form.fields.keys())}")
        else:
            print("❌ No users found to test password form")
    except Exception as e:
        print(f"❌ Error testing password form: {e}")
    
    print("\n🎉 User management system test completed!")
    return True

if __name__ == "__main__":
    test_user_management_system()