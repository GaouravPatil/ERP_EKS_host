"""
Management command to populate database with dynamic choices
"""
from django.core.management.base import BaseCommand
from college_erp.choices import ChoiceCategory, Choice


class Command(BaseCommand):
    help = 'Populate database with dynamic choices replacing hardcoded values'
    
    def handle(self, *args, **options):
        self.stdout.write('Populating dynamic choices...')
        
        # Define all choices data
        choices_data = {
            'user_types': {
                'description': 'Types of users in the system',
                'choices': [
                    ('admin', 'Administrator', 1),
                    ('teacher', 'Teacher', 2),
                    ('student', 'Student', 3),
                ]
            },
            'notification_types': {
                'description': 'Types of notifications',
                'choices': [
                    ('general', 'General', 1),
                    ('academic', 'Academic', 2),
                    ('exam', 'Exam', 3),
                    ('fee', 'Fee', 4),
                    ('event', 'Event', 5),
                    ('urgent', 'Urgent', 6),
                ]
            },
            'qualifications': {
                'description': 'Educational qualifications for teachers',
                'choices': [
                    ('bachelor', "Bachelor's Degree", 1),
                    ('master', "Master's Degree", 2),
                    ('phd', 'Ph.D.', 3),
                    ('diploma', 'Diploma', 4),
                    ('certification', 'Professional Certification', 5),
                    ('other', 'Other', 6),
                ]
            },
            'employment_types': {
                'description': 'Types of employment for teachers',
                'choices': [
                    ('permanent', 'Permanent', 1),
                    ('contract', 'Contract', 2),
                    ('visiting', 'Visiting', 3),
                    ('guest', 'Guest Faculty', 4),
                    ('part_time', 'Part Time', 5),
                ]
            },
            'semesters': {
                'description': 'Academic semesters',
                'choices': [
                    ('1', '1st Semester', 1),
                    ('2', '2nd Semester', 2),
                    ('3', '3rd Semester', 3),
                    ('4', '4th Semester', 4),
                    ('5', '5th Semester', 5),
                    ('6', '6th Semester', 6),
                    ('7', '7th Semester', 7),
                    ('8', '8th Semester', 8),
                ]
            },
            'fee_types': {
                'description': 'Types of fees',
                'choices': [
                    ('tuition', 'Tuition Fee', 1),
                    ('library', 'Library Fee', 2),
                    ('lab', 'Laboratory Fee', 3),
                    ('exam', 'Examination Fee', 4),
                    ('development', 'Development Fee', 5),
                    ('sports', 'Sports Fee', 6),
                    ('transport', 'Transport Fee', 7),
                    ('hostel', 'Hostel Fee', 8),
                    ('miscellaneous', 'Miscellaneous Fee', 9),
                    ('other', 'Other Fee', 10),
                ]
            },
            'payment_status': {
                'description': 'Payment status for fees',
                'choices': [
                    ('pending', 'Pending', 1),
                    ('paid', 'Paid', 2),
                    ('partial', 'Partially Paid', 3),
                    ('overdue', 'Overdue', 4),
                    ('cancelled', 'Cancelled', 5),
                    ('refunded', 'Refunded', 6),
                ]
            },
            'exam_types': {
                'description': 'Types of exams and assessments',
                'choices': [
                    ('quiz', 'Quiz', 1),
                    ('assignment', 'Assignment', 2),
                    ('midterm', 'Mid-term Exam', 3),
                    ('final', 'Final Exam', 4),
                    ('project', 'Project', 5),
                    ('presentation', 'Presentation', 6),
                    ('practical', 'Practical Exam', 7),
                    ('viva', 'Viva Voce', 8),
                ]
            },
            'priority_levels': {
                'description': 'Priority levels for notifications and tasks',
                'choices': [
                    ('low', 'Low', 1),
                    ('medium', 'Medium', 2),
                    ('high', 'High', 3),
                    ('urgent', 'Urgent', 4),
                    ('critical', 'Critical', 5),
                ]
            },
            'recipient_types': {
                'description': 'Types of notification recipients',
                'choices': [
                    ('all', 'All Users', 1),
                    ('students', 'All Students', 2),
                    ('teachers', 'All Teachers', 3),
                    ('admins', 'All Administrators', 4),
                    ('specific', 'Specific Users', 5),
                    ('class', 'Specific Class', 6),
                    ('department', 'Specific Department', 7),
                ]
            },
            'weekdays': {
                'description': 'Days of the week for timetable',
                'choices': [
                    ('monday', 'Monday', 1),
                    ('tuesday', 'Tuesday', 2),
                    ('wednesday', 'Wednesday', 3),
                    ('thursday', 'Thursday', 4),
                    ('friday', 'Friday', 5),
                    ('saturday', 'Saturday', 6),
                    ('sunday', 'Sunday', 7),
                ]
            },
            'target_audience': {
                'description': 'Target audience for notifications',
                'choices': [
                    ('all', 'All Students', 1),
                    ('class', 'Specific Class', 2),
                    ('department', 'Specific Department', 3),
                    ('individual', 'Individual Student', 4),
                    ('batch', 'Specific Batch', 5),
                    ('year', 'Specific Year', 6),
                ]
            },
            'grade_types': {
                'description': 'Grade scales for exams',
                'choices': [
                    ('a_plus', 'A+', 1),
                    ('a', 'A', 2),
                    ('b_plus', 'B+', 3),
                    ('b', 'B', 4),
                    ('c_plus', 'C+', 5),
                    ('c', 'C', 6),
                    ('d', 'D', 7),
                    ('f', 'F', 8),
                ]
            },
        }
        
        created_count = 0
        updated_count = 0
        
        for category_name, category_data in choices_data.items():
            # Create or get category
            category, created = ChoiceCategory.objects.get_or_create(
                name=category_name,
                defaults={
                    'description': category_data['description'],
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(f'Created category: {category_name}')
                created_count += 1
            else:
                category.description = category_data['description']
                category.save()
                updated_count += 1
            
            # Create choices for this category
            for value, label, order in category_data['choices']:
                choice, created = Choice.objects.get_or_create(
                    category=category,
                    value=value,
                    defaults={
                        'label': label,
                        'order': order,
                        'is_active': True
                    }
                )
                
                if created:
                    self.stdout.write(f'  Created choice: {label}')
                    created_count += 1
                else:
                    # Update existing choice
                    choice.label = label
                    choice.order = order
                    choice.save()
                    updated_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully populated choices. '
                f'Created: {created_count}, Updated: {updated_count}'
            )
        )