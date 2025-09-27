from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from academics.models import Department, Course, Class
from datetime import date

User = get_user_model()

class Command(BaseCommand):
    help = 'Add MIT-WPU department data to the system'

    def handle(self, *args, **options):
        self.stdout.write('Adding MIT-WPU departments...')
        
        # MIT-WPU Departments data
        departments_data = [
            {
                'name': 'WPU School of Engineering & Technology',
                'code': 'SET',
                'description': 'School of Engineering & Technology offering various engineering disciplines including Mechanical, Civil, Electrical, and Electronics & Communication Engineering.',
            },
            {
                'name': 'WPU School of Computer Science & Engineering',
                'code': 'SCSE',
                'description': 'School of Computer Science & Engineering focusing on Computer Science, Information Technology, Data Science, and Artificial Intelligence programs.',
            },
            {
                'name': 'Ramcharan School of Leadership',
                'code': 'RSL',
                'description': 'Dedicated to developing leadership skills and management capabilities through specialized programs and workshops.',
            },
            {
                'name': 'WPU School of Business',
                'code': 'SOB',
                'description': 'School of Business offering MBA, BBA, and specialized business programs with focus on entrepreneurship and innovation.',
            },
            {
                'name': 'WPU School of Economics & Commerce',
                'code': 'SEC',
                'description': 'School of Economics & Commerce providing undergraduate and postgraduate programs in Economics, Commerce, and related fields.',
            },
            {
                'name': 'MIT School of Government',
                'code': 'SOG',
                'description': 'School of Government focusing on public administration, policy studies, and governance programs.',
            },
            {
                'name': 'WPU School of Health Sciences & Technology',
                'code': 'SHST',
                'description': 'School of Health Sciences & Technology offering programs in Medical Technology, Physiotherapy, Pharmacy, and Healthcare Management.',
            },
            {
                'name': 'WPU School of Science & Environmental Studies',
                'code': 'SSES',
                'description': 'School of Science & Environmental Studies providing programs in Pure Sciences, Applied Sciences, and Environmental Studies.',
            },
            {
                'name': 'WPU School of Design',
                'code': 'SOD',
                'description': 'School of Design offering creative programs in Fashion Design, Interior Design, Product Design, and Visual Communication.',
            },
            {
                'name': 'WPU School of Liberal Arts',
                'code': 'SLA',
                'description': 'School of Liberal Arts providing interdisciplinary programs in Humanities, Social Sciences, and Liberal Studies.',
            },
            {
                'name': 'WPU School of Law',
                'code': 'SOL',
                'description': 'School of Law offering undergraduate and postgraduate law programs with emphasis on contemporary legal practices.',
            },
            {
                'name': 'WPU School of Consciousness',
                'code': 'SOC',
                'description': 'School of Consciousness focusing on holistic education, mindfulness, and consciousness studies programs.',
            },
        ]
        
        created_count = 0
        updated_count = 0
        
        for dept_data in departments_data:
            department, created = Department.objects.get_or_create(
                code=dept_data['code'],
                defaults={
                    'name': dept_data['name'],
                    'description': dept_data['description'],
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(f'  ✅ Created: {department.name}')
            else:
                # Update existing department
                department.name = dept_data['name']
                department.description = dept_data['description']
                department.save()
                updated_count += 1
                self.stdout.write(f'  🔄 Updated: {department.name}')
        
        # Create sample courses for some departments
        sample_courses = [
            # Engineering & Technology
            ('SET', [
                ('Mechanical Engineering Fundamentals', 'ME101', 'Introduction to Mechanical Engineering principles'),
                ('Electrical Circuits', 'EE101', 'Basic electrical circuit analysis and design'),
                ('Engineering Mathematics', 'MA101', 'Mathematical foundations for engineering'),
            ]),
            # Computer Science & Engineering
            ('SCSE', [
                ('Programming Fundamentals', 'CS101', 'Introduction to programming concepts'),
                ('Data Structures and Algorithms', 'CS201', 'Core data structures and algorithmic thinking'),
                ('Database Management Systems', 'CS301', 'Database design and management'),
                ('Artificial Intelligence', 'CS401', 'Introduction to AI and machine learning'),
            ]),
            # Business
            ('SOB', [
                ('Principles of Management', 'MGT101', 'Fundamental management principles and practices'),
                ('Financial Accounting', 'ACC101', 'Basic accounting principles and financial statements'),
                ('Marketing Management', 'MKT201', 'Marketing strategies and consumer behavior'),
                ('Entrepreneurship', 'ENT301', 'Innovation and entrepreneurial thinking'),
            ]),
            # Economics & Commerce
            ('SEC', [
                ('Microeconomics', 'ECO101', 'Individual economic behavior and market analysis'),
                ('Macroeconomics', 'ECO201', 'National economy and policy analysis'),
                ('Business Statistics', 'STA101', 'Statistical methods for business decisions'),
                ('International Trade', 'ECO301', 'Global trade theories and practices'),
            ]),
            # Health Sciences & Technology
            ('SHST', [
                ('Human Anatomy', 'MED101', 'Structure and function of human body'),
                ('Pharmacology', 'PHAR201', 'Drug action and therapeutic applications'),
                ('Medical Technology', 'MT301', 'Medical equipment and diagnostic techniques'),
                ('Healthcare Management', 'HM401', 'Healthcare systems and administration'),
            ]),
            # Design
            ('SOD', [
                ('Design Fundamentals', 'DES101', 'Basic principles of design and creativity'),
                ('Fashion Design', 'FD201', 'Fashion illustration and garment construction'),
                ('Interior Design', 'ID301', 'Space planning and interior decoration'),
                ('Visual Communication', 'VC401', 'Graphic design and visual storytelling'),
            ]),
        ]
        
        courses_created = 0
        for dept_code, courses in sample_courses:
            try:
                department = Department.objects.get(code=dept_code)
                for course_name, course_code, description in courses:
                    course, created = Course.objects.get_or_create(
                        code=course_code,
                        defaults={
                            'name': course_name,
                            'department': department,
                            'semester': 1,
                            'credits': 4,
                            'description': description,
                        }
                    )
                    if created:
                        courses_created += 1
            except Department.DoesNotExist:
                continue
        
        # Create sample classes for major departments
        major_departments = ['SET', 'SCSE', 'SOB', 'SEC', 'SHST', 'SOD']
        classes_created = 0
        
        for dept_code in major_departments:
            try:
                department = Department.objects.get(code=dept_code)
                for year in ['2024-2025', '2023-2024']:
                    for semester in [1, 2]:
                        for section in ['A', 'B']:
                            class_name = f'{dept_code} - Year {year.split("-")[0]} - Sem {semester} - Section {section}'
                            class_obj, created = Class.objects.get_or_create(
                                name=class_name,
                                department=department,
                                semester=semester,
                                section=section,
                                academic_year=year,
                                defaults={
                                    'max_strength': 60,
                                }
                            )
                            if created:
                                classes_created += 1
            except Department.DoesNotExist:
                continue
        
        self.stdout.write(
            self.style.SUCCESS(f'\n🎉 MIT-WPU departments setup completed!')
        )
        self.stdout.write(f'📊 Summary:')
        self.stdout.write(f'  • {created_count} new departments created')
        self.stdout.write(f'  • {updated_count} departments updated')
        self.stdout.write(f'  • {courses_created} sample courses created')
        self.stdout.write(f'  • {classes_created} sample classes created')
        
        self.stdout.write(f'\n🏫 All MIT-WPU Schools:')
        for dept in Department.objects.all().order_by('code'):
            self.stdout.write(f'  • {dept.code}: {dept.name}')
        
        self.stdout.write(f'\n✨ Your College ERP now supports all MIT-WPU schools!')
        self.stdout.write(f'💡 Access the admin dashboard to see the updated department statistics.')