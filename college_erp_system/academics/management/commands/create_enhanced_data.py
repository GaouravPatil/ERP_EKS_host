from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from academics.models import Department, Course, Class, Subject, Attendance, Exam, Result, Fee, TimeSlot, Timetable
from students.models import Student, Notification
from teachers.models import Teacher
from datetime import date, datetime, timedelta
from django.utils import timezone
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Create enhanced sample data with attendance, exams, fees, and MIT-WPU departments'

    def create_mitwpu_departments(self):
        """Create all MIT-WPU departments"""
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
        
        # Create sample courses for MIT-WPU departments with actual course offerings
        sample_courses = [
            # School of Engineering & Technology
            ('SET', [
                # B.Tech Programs
                ('Civil Engineering', 'CE101', 'Bachelor of Technology in Civil Engineering with focus on construction and infrastructure'),
                ('Mechanical Engineering', 'ME101', 'Bachelor of Technology in Mechanical Engineering covering thermodynamics, mechanics, and manufacturing'),
                ('Chemical Engineering', 'CHE101', 'Bachelor of Technology in Chemical Engineering with process engineering and materials'),
                ('Materials Science & Engineering', 'MSE101', 'Bachelor of Technology in Materials Science focusing on material properties and applications'),
                ('Electrical & Electronics Engineering', 'EEE101', 'Bachelor of Technology in Electrical & Electronics Engineering'),
                ('Petroleum Engineering', 'PE101', 'Bachelor of Technology in Petroleum Engineering with oil and gas industry focus'),
                ('Bioengineering', 'BE101', 'Bachelor of Technology in Bioengineering combining biology and engineering principles'),
                ('Electronics & Communication Engineering', 'ECE101', 'Bachelor of Technology in Electronics & Communication Engineering'),
                # M.Tech Programs
                ('M.Tech Chemical Engineering', 'CHE201', 'Master of Technology in Chemical Engineering with advanced process design'),
                ('Construction Engineering & Management', 'CEM201', 'Master of Technology in Civil Engineering with construction focus'),
                ('Environmental Engineering', 'ENV201', 'Master of Technology in Environmental Engineering'),
                ('VLSI & Embedded Systems', 'VES201', 'Master of Technology in Electronics & Communication (VLSI & Embedded Systems)'),
                ('e-Mobility', 'EM201', 'Master of Technology in e-Mobility and sustainable transportation'),
                # Ph.D Programs
                ('Ph.D Civil Engineering', 'CE301', 'Doctor of Philosophy in Civil Engineering research'),
                ('Ph.D Chemical Engineering', 'CHE301', 'Doctor of Philosophy in Chemical Engineering research'),
                ('Ph.D Electronics & Communication', 'ECE301', 'Doctor of Philosophy in Electronics & Communication Engineering'),
            ]),
            
            # School of Computer Science & Engineering
            ('SCSE', [
                # B.Tech Programs
                ('Computer Science & Engineering', 'CSE101', 'Bachelor of Technology in Computer Science & Engineering'),
                ('CSE with Cyber Security & Forensics', 'CSF101', 'B.Tech CSE specializing in Cyber Security & Forensics'),
                ('CSE with Cloud Computing', 'CCC101', 'B.Tech CSE specializing in Cloud Computing technologies'),
                ('CSE with AI & Data Science', 'ADS101', 'B.Tech CSE specializing in Artificial Intelligence & Data Science'),
                # B.Sc Programs
                ('Computer Science', 'CS101', 'Bachelor of Science in Computer Science with programming fundamentals'),
                ('Bachelor of Computer Applications', 'BCA101', 'BCA program covering software development and applications'),
                # M.Sc/M.Tech Programs
                ('M.Sc Computer Science', 'CS201', 'Master of Science in Computer Science with advanced computing concepts'),
                ('M.Tech CSE Data Science & Analytics', 'DSA201', 'Master of Technology in CSE specializing in Data Science & Analytics'),
                ('Master of Computer Applications', 'MCA201', 'MCA program with advanced software development'),
                # Ph.D Programs
                ('Ph.D Computer Science', 'CS301', 'Doctor of Philosophy in Computer Science research'),
            ]),
            
            # School of Business
            ('SOB', [
                # BBA Programs
                ('BBA Digital Marketing', 'BDM101', 'Bachelor of Business Administration specializing in Digital Marketing'),
                ('BBA Business Analytics', 'BBA101', 'Bachelor of Business Administration specializing in Business Analytics'),
                ('BBA Global Business', 'BGB101', 'Bachelor of Business Administration specializing in Global Business'),
                ('Integrated BBA+MBA', 'IBM101', 'Integrated BBA+MBA program for comprehensive business education'),
                # MBA Programs
                ('MBA Finance', 'MBA201', 'Master of Business Administration specializing in Finance'),
                ('MBA Marketing', 'MBM201', 'Master of Business Administration specializing in Marketing'),
                ('MBA Human Resources', 'MBH201', 'Master of Business Administration specializing in Human Resources'),
                ('MBA Operations', 'MBO201', 'Master of Business Administration specializing in Operations Management'),
                ('MBA International Business', 'MBI201', 'Master of Business Administration specializing in International Business'),
            ]),
            
            # School of Economics & Commerce
            ('SEC', [
                # B.Com Programs
                ('B.Com International Accounting & Finance', 'IAF101', 'Bachelor of Commerce in International Accounting & Finance'),
                ('B.Com Fintech', 'FIN101', 'Bachelor of Commerce specializing in Financial Technology'),
                ('B.Com Advanced Accounting & Auditing', 'AAA101', 'Bachelor of Commerce in Advanced Accounting & Auditing'),
                ('B.Com General', 'COM101', 'Bachelor of Commerce with comprehensive business knowledge'),
                # Economics Programs
                ('Economics (UG)', 'ECO101', 'Undergraduate program in Economics with macro and micro economics'),
                ('Economics (PG)', 'ECO201', 'Postgraduate program in Economics with advanced economic theory'),
                # M.Com Programs
                ('M.Com Finance', 'MCF201', 'Master of Commerce specializing in Finance'),
                ('M.Com Accounting', 'MCA201', 'Master of Commerce specializing in Accounting'),
                # Ph.D Programs
                ('Ph.D Commerce', 'COM301', 'Doctor of Philosophy in Commerce research'),
            ]),
            
            # School of Health Sciences & Technology
            ('SHST', [
                # B.Pharm Programs
                ('Bachelor of Pharmacy', 'BPH101', 'Bachelor of Pharmacy with pharmaceutical sciences foundation'),
                # M.Pharm Programs
                ('M.Pharm Pharmaceutical Chemistry', 'MPC201', 'Master of Pharmacy specializing in Pharmaceutical Chemistry'),
                ('M.Pharm Pharmaceutics', 'MPH201', 'Master of Pharmacy specializing in Pharmaceutics'),
                ('M.Pharm Pharmacology', 'MPL201', 'Master of Pharmacy specializing in Pharmacology'),
                ('M.Pharm Quality Assurance', 'MQA201', 'Master of Pharmacy specializing in Quality Assurance'),
                # Pharm.D Programs
                ('Doctor of Pharmacy', 'PHD101', 'Doctor of Pharmacy (Pharm.D) clinical pharmacy program'),
                # Public Health Programs
                ('Masters of Public Health', 'MPH201', 'Masters of Public Health with community health focus'),
                ('Health Sciences', 'HS101', 'Undergraduate program in Health Sciences'),
                # Allied Health Programs
                ('Medical Technology', 'MT101', 'Bachelor program in Medical Technology and diagnostics'),
                ('Physiotherapy', 'PT101', 'Bachelor of Physiotherapy for rehabilitation sciences'),
            ]),
            
            # School of Science & Environmental Studies
            ('SSES', [
                # B.Sc Programs
                ('B.Sc Physics', 'PHY101', 'Bachelor of Science in Physics with theoretical and applied physics'),
                ('B.Sc Chemistry', 'CHM101', 'Bachelor of Science in Chemistry with organic, inorganic, and physical chemistry'),
                ('B.Sc Biosciences', 'BIO101', 'Bachelor of Science in Biosciences covering biology and life sciences'),
                ('B.Sc Applied Statistics', 'STA101', 'Bachelor of Science in Applied Statistics with data analysis'),
                ('B.Sc Environmental Science', 'ENV101', 'Bachelor of Science in Environmental Science and sustainability'),
                ('B.Sc Mathematics', 'MTH101', 'Bachelor of Science in Mathematics with pure and applied mathematics'),
                # M.Sc Programs
                ('M.Sc Physics', 'PHY201', 'Master of Science in Physics with advanced physics concepts'),
                ('M.Sc Chemistry', 'CHM201', 'Master of Science in Chemistry with research methodology'),
                ('M.Sc Environmental Studies', 'ENV201', 'Master of Science in Environmental Studies'),
                ('M.Sc Biosciences', 'BIO201', 'Master of Science in Biosciences with molecular biology'),
                # Ph.D Programs
                ('Ph.D Physics', 'PHY301', 'Doctor of Philosophy in Physics research'),
                ('Ph.D Chemistry', 'CHM301', 'Doctor of Philosophy in Chemistry research'),
                ('Ph.D Environmental Science', 'ENV301', 'Doctor of Philosophy in Environmental Science research'),
            ]),
            
            # School of Design
            ('SOD', [
                # B.Des Programs
                ('B.Des Animation & VFX', 'AVX101', 'Bachelor of Design in Animation & Visual Effects'),
                ('B.Des Fashion & Apparel', 'FA101', 'Bachelor of Design in Fashion & Apparel Design'),
                ('B.Des Interior & Space', 'IS101', 'Bachelor of Design in Interior & Space Design'),
                ('B.Des Product Design', 'PD101', 'Bachelor of Design in Product Design and Innovation'),
                ('B.Des UX Design', 'UX101', 'Bachelor of Design in User Experience Design'),
                ('B.Des Visual Communication', 'VC101', 'Bachelor of Design in Visual Communication'),
                ('B.Des Graphic Design', 'GD101', 'Bachelor of Design in Graphic Design'),
                # M.Des Programs
                ('M.Des Industrial Design', 'ID201', 'Master of Design in Industrial Design'),
                ('M.Des UX Design', 'UX201', 'Master of Design in User Experience Design'),
                ('M.Des Fashion Design', 'FD201', 'Master of Design in Fashion Design'),
                # Ph.D Programs
                ('Ph.D Design', 'DES301', 'Doctor of Philosophy in Design research and innovation'),
            ]),
            
            # School of Liberal Arts & Humanities
            ('SLA', [
                # BA Programs
                ('BA English', 'ENG101', 'Bachelor of Arts in English Literature and Language'),
                ('BA Psychology', 'PSY101', 'Bachelor of Arts in Psychology with human behavior studies'),
                ('BA Political Science', 'POL101', 'Bachelor of Arts in Political Science and governance'),
                ('BA Media & Communication', 'MC101', 'Bachelor of Arts in Media & Communication Studies'),
                ('BA Photography', 'PHO101', 'Bachelor of Arts in Photography and Visual Arts'),
                ('BA Filmmaking', 'FM101', 'Bachelor of Arts in Filmmaking and Cinema Studies'),
                # MA Programs
                ('MA English', 'ENG201', 'Master of Arts in English with advanced literature studies'),
                ('MA Psychology', 'PSY201', 'Master of Arts in Psychology with research methodology'),
                ('MA Political Science', 'POL201', 'Master of Arts in Political Science'),
                ('MA Media & Communication', 'MC201', 'Master of Arts in Media & Communication'),
                # Education Programs
                ('Bachelor of Education', 'BED101', 'B.Ed program for teaching profession'),
                ('Master of Education', 'MED201', 'M.Ed program with educational research and pedagogy'),
            ]),
            
            # School of Law
            ('SOL', [
                # Law Programs
                ('Bachelor of Laws', 'LLB101', 'LL.B. program with comprehensive legal education'),
                ('BA LL.B (Hons)', 'BLL101', 'BA LL.B (Hons) integrated law program'),
                ('BBA LL.B (Hons)', 'BBL101', 'BBA LL.B (Hons) integrated business law program'),
                ('Master of Laws', 'LLM201', 'LL.M program with specialized legal studies'),
                ('Constitutional Law', 'CON101', 'Specialized course in Constitutional Law'),
                ('Criminal Law', 'CRM101', 'Specialized course in Criminal Law and Procedure'),
                ('Corporate Law', 'CRP101', 'Specialized course in Corporate Law and Governance'),
                ('International Law', 'INT101', 'Specialized course in International Law'),
                ('Cyber Law', 'CYB101', 'Specialized course in Cyber Law and Digital Rights'),
            ]),
            
            # School of Government
            ('SOG', [
                # Government Programs
                ('BA Government and Administration', 'GA101', 'Bachelor of Arts in Government and Public Administration'),
                ('MA Political Leadership & Government', 'PLG201', 'Master of Arts in Political Leadership & Government'),
                ('Public Policy', 'PP101', 'Undergraduate program in Public Policy Analysis'),
                ('Governance Studies', 'GS101', 'Program in Governance and Administrative Studies'),
                ('International Relations', 'IR101', 'Program in International Relations and Diplomacy'),
                ('Public Administration', 'PA101', 'Program in Public Administration and Management'),
            ]),
            
            # Ramcharan School of Leadership
            ('RSL', [
                # Leadership Programs
                ('Leadership Studies', 'LS101', 'Undergraduate program in Leadership and Management'),
                ('Executive Leadership', 'EL201', 'Postgraduate program in Executive Leadership'),
                ('Social Leadership', 'SL101', 'Program in Social Leadership and Community Development'),
                ('Corporate Leadership', 'CL101', 'Program in Corporate Leadership and Strategy'),
                ('Entrepreneurial Leadership', 'ENL101', 'Program in Entrepreneurial Leadership and Innovation'),
            ]),
            
            # School of Consciousness
            ('SOC', [
                # Consciousness Studies Programs
                ('Ph.D Consciousness Studies', 'CS301', 'Doctor of Philosophy in Consciousness Studies research'),
                ('Consciousness & Spirituality', 'CS101', 'Undergraduate program in Consciousness & Spirituality'),
                ('Mindfulness Studies', 'MS101', 'Program in Mindfulness and Meditation Studies'),
                ('Philosophy of Consciousness', 'PC201', 'Postgraduate program in Philosophy of Consciousness'),
                ('Applied Consciousness Studies', 'ACS101', 'Program in Applied Consciousness Studies'),
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
        major_departments = ['SET', 'SCSE', 'SOB', 'SEC', 'SHST', 'SOD', 'SLA', 'SOL']
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
        
        self.stdout.write(f'🏫 MIT-WPU Departments: {created_count} created, {updated_count} updated')
        self.stdout.write(f'📚 Courses: {courses_created} created')
        self.stdout.write(f'🏛️ Classes: {classes_created} created')
        
        return created_count, updated_count

    def create_hod_privileges(self):
        """Create additional privileges and information for HODs"""
        hods = User.objects.filter(headed_departments__isnull=False).distinct()
        
        for hod in hods:
            try:
                teacher_profile = hod.teacher_profile
                department = hod.headed_departments.first()
                
                # Update HOD specific details
                if not teacher_profile.research_interests:
                    teacher_profile.research_interests = f'Department Leadership, Academic Administration, {department.name} Research'
                
                # Update office hours for administrative duties
                teacher_profile.office_hours = '9:00 AM - 5:00 PM (Administrative Hours)'
                
                # Ensure they have a dedicated office room
                if not teacher_profile.office_room or 'Room-' in teacher_profile.office_room:
                    teacher_profile.office_room = f'HOD Office - {department.code}'
                
                # Update designation to include HOD title
                if 'HOD' not in teacher_profile.designation:
                    teacher_profile.designation = f'{teacher_profile.designation} & HOD'
                
                teacher_profile.save()
                
            except Exception as e:
                self.stdout.write(f'Warning: Could not update HOD privileges for {hod.get_full_name()}: {e}')
        
        self.stdout.write(f'📋 HOD Privileges: Updated administrative details for {len(hods)} HODs')

    def handle(self, *args, **options):
        self.stdout.write('Creating enhanced sample data with MIT-WPU departments...')
        
        # First, add all MIT-WPU departments
        self.create_mitwpu_departments()
        
        # Get existing data
        try:
            cs_dept = Department.objects.get(code='CS')
            student_user = User.objects.get(username='student1')
            teacher_user = User.objects.get(username='teacher1')
            student = Student.objects.get(user=student_user)
            teacher = Teacher.objects.get(user=teacher_user)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Please run create_sample_data first: {e}'))
            return
        
        # Create 30 students for each course
        self.stdout.write('Creating 30 students per course...')
        
        # Get all courses
        all_courses = Course.objects.all()
        student_counter = 1
        students_created = 0
        
        # Common Indian first names for variety
        indian_first_names = [
            'Aarav', 'Vivaan', 'Aditya', 'Vihaan', 'Arjun', 'Sai', 'Reyansh', 'Ayaan', 'Krishna', 'Ishaan',
            'Shaurya', 'Atharv', 'Advik', 'Rudra', 'Ahaan', 'Ananya', 'Saanvi', 'Aadhya', 'Kiara', 'Diya',
            'Kavya', 'Aarohi', 'Avni', 'Pari', 'Ira', 'Myra', 'Anika', 'Riya', 'Shreya', 'Navya',
            'Priya', 'Meera', 'Sia', 'Tara', 'Zara', 'Nisha', 'Aditi', 'Pooja', 'Sneha', 'Divya',
            'Rahul', 'Rohan', 'Karan', 'Varun', 'Nikhil', 'Harsh', 'Dev', 'Yash', 'Kartik', 'Ravi'
        ]
        
        indian_last_names = [
            'Sharma', 'Patel', 'Singh', 'Kumar', 'Gupta', 'Agarwal', 'Jain', 'Mehta', 'Shah', 'Reddy',
            'Nair', 'Iyer', 'Rao', 'Pillai', 'Menon', 'Desai', 'Trivedi', 'Joshi', 'Pandey', 'Mishra',
            'Tiwari', 'Saxena', 'Bansal', 'Malhotra', 'Khanna', 'Chopra', 'Arora', 'Kapoor', 'Verma', 'Sinha'
        ]
        
        # Indian cities for addresses
        indian_cities = [
            'Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune', 'Ahmedabad',
            'Jaipur', 'Lucknow', 'Kanpur', 'Nagpur', 'Indore', 'Thane', 'Bhopal', 'Visakhapatnam',
            'Patna', 'Vadodara', 'Ghaziabad', 'Ludhiana', 'Agra', 'Nashik', 'Faridabad', 'Meerut'
        ]
        
        for course in all_courses:
            # Get classes for this course's department
            available_classes = Class.objects.filter(department=course.department)
            if not available_classes:
                continue
                
            # Create 30 students for this course
            for i in range(30):
                first_name = random.choice(indian_first_names)
                last_name = random.choice(indian_last_names)
                city = random.choice(indian_cities)
                
                # Create unique username based on course code and student number
                username = f'{course.code.lower()}_student_{i+1}'
                email = f'{username}@mitwpu.edu.in'
                
                user, created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        'first_name': first_name,
                        'last_name': last_name,
                        'email': email,
                        'user_type': 'student'
                    }
                )
                
                if created:
                    user.set_password('student123')
                    user.save()
                    
                    # Generate roll number based on course and year
                    current_year = datetime.now().year
                    roll_number = f'{course.code}{str(current_year)[2:]}{str(i+1).zfill(3)}'
                    admission_number = f'MIT{current_year}{str(student_counter).zfill(4)}'
                    
                    # Assign to a random class from the course's department
                    assigned_class = random.choice(available_classes)
                    
                    Student.objects.get_or_create(
                        user=user,
                        defaults={
                            'roll_number': roll_number,
                            'admission_number': admission_number,
                            'student_class': assigned_class,
                            'department': course.department,
                            'admission_date': date(current_year, random.randint(1, 8), random.randint(1, 28)),
                            'guardian_name': f'{random.choice(indian_first_names)} {last_name}',
                            'guardian_phone': f'{random.randint(7000000000, 9999999999)}',
                            'guardian_email': f'guardian_{username}@email.com',
                            'guardian_address': f'{random.randint(1, 999)} {random.choice(["MG Road", "Park Street", "Main Road", "Gandhi Road", "Nehru Street"])}, {city}',
                            'emergency_contact': f'{random.randint(7000000000, 9999999999)}',
                            'blood_group': random.choice(['A+', 'B+', 'O+', 'AB+', 'A-', 'B-', 'O-', 'AB-']),
                        }
                    )
                    
                    student_counter += 1
                    students_created += 1
                    
                    # Progress indicator for large data creation
                    if students_created % 100 == 0:
                        self.stdout.write(f'  Created {students_created} students so far...')
        
        self.stdout.write(f'👥 Students: {students_created} created across all courses')
        
        # Create comprehensive teachers and subjects for all courses
        self.stdout.write('Creating teachers and subjects for all courses...')
        
        # Teacher names and qualifications data
        teacher_data = [
            # Engineering Faculty
            ('Dr. Rajesh Kumar', 'PhD in Mechanical Engineering', 'Professor', '15 years', 'rajesh.kumar@mitwpu.edu.in'),
            ('Dr. Priya Sharma', 'PhD in Civil Engineering', 'Associate Professor', '12 years', 'priya.sharma@mitwpu.edu.in'),
            ('Dr. Amit Patel', 'PhD in Chemical Engineering', 'Professor', '18 years', 'amit.patel@mitwpu.edu.in'),
            ('Dr. Neha Gupta', 'PhD in Electrical Engineering', 'Assistant Professor', '8 years', 'neha.gupta@mitwpu.edu.in'),
            ('Prof. Vikram Singh', 'M.Tech in Materials Science', 'Associate Professor', '10 years', 'vikram.singh@mitwpu.edu.in'),
            ('Dr. Kavita Reddy', 'PhD in Petroleum Engineering', 'Professor', '14 years', 'kavita.reddy@mitwpu.edu.in'),
            ('Dr. Suresh Nair', 'PhD in Bioengineering', 'Associate Professor', '11 years', 'suresh.nair@mitwpu.edu.in'),
            ('Prof. Anita Joshi', 'M.Tech in Electronics', 'Assistant Professor', '7 years', 'anita.joshi@mitwpu.edu.in'),
            
            # Computer Science Faculty
            ('Dr. Rahul Mehta', 'PhD in Computer Science', 'Professor', '16 years', 'rahul.mehta@mitwpu.edu.in'),
            ('Dr. Sneha Verma', 'PhD in Artificial Intelligence', 'Associate Professor', '9 years', 'sneha.verma@mitwpu.edu.in'),
            ('Prof. Kiran Desai', 'M.Tech in Data Science', 'Assistant Professor', '6 years', 'kiran.desai@mitwpu.edu.in'),
            ('Dr. Arun Trivedi', 'PhD in Cyber Security', 'Professor', '13 years', 'arun.trivedi@mitwpu.edu.in'),
            ('Prof. Pooja Bansal', 'M.Sc in Computer Science', 'Associate Professor', '8 years', 'pooja.bansal@mitwpu.edu.in'),
            ('Dr. Manoj Agarwal', 'PhD in Cloud Computing', 'Assistant Professor', '5 years', 'manoj.agarwal@mitwpu.edu.in'),
            
            # Business Faculty  
            ('Dr. Sanjay Khanna', 'PhD in Business Administration', 'Professor', '20 years', 'sanjay.khanna@mitwpu.edu.in'),
            ('Prof. Deepa Chopra', 'MBA in Finance', 'Associate Professor', '12 years', 'deepa.chopra@mitwpu.edu.in'),
            ('Dr. Ravi Malhotra', 'PhD in Marketing', 'Professor', '17 years', 'ravi.malhotra@mitwpu.edu.in'),
            ('Prof. Sunita Kapoor', 'MBA in HR', 'Assistant Professor', '9 years', 'sunita.kapoor@mitwpu.edu.in'),
            ('Dr. Ashish Arora', 'PhD in Operations', 'Associate Professor', '11 years', 'ashish.arora@mitwpu.edu.in'),
            
            # Economics & Commerce Faculty
            ('Dr. Vijay Saxena', 'PhD in Economics', 'Professor', '19 years', 'vijay.saxena@mitwpu.edu.in'),
            ('Prof. Meera Tiwari', 'M.Com, CA', 'Associate Professor', '13 years', 'meera.tiwari@mitwpu.edu.in'),
            ('Dr. Ramesh Pandey', 'PhD in Commerce', 'Professor', '15 years', 'ramesh.pandey@mitwpu.edu.in'),
            ('Prof. Geeta Mishra', 'M.Com in Finance', 'Assistant Professor', '7 years', 'geeta.mishra@mitwpu.edu.in'),
            
            # Health Sciences Faculty
            ('Dr. Sunil Rao', 'PhD in Pharmacy', 'Professor', '18 years', 'sunil.rao@mitwpu.edu.in'),
            ('Dr. Lakshmi Pillai', 'Pharm.D, PhD', 'Associate Professor', '12 years', 'lakshmi.pillai@mitwpu.edu.in'),
            ('Prof. Prakash Menon', 'M.Pharm', 'Assistant Professor', '8 years', 'prakash.menon@mitwpu.edu.in'),
            ('Dr. Shanti Iyer', 'PhD in Public Health', 'Professor', '16 years', 'shanti.iyer@mitwpu.edu.in'),
            ('Prof. Raman Nair', 'M.Pharm in Pharmacology', 'Associate Professor', '10 years', 'raman.nair@mitwpu.edu.in'),
            
            # Science Faculty
            ('Dr. Mohan Das', 'PhD in Physics', 'Professor', '21 years', 'mohan.das@mitwpu.edu.in'),
            ('Dr. Usha Sinha', 'PhD in Chemistry', 'Associate Professor', '14 years', 'usha.sinha@mitwpu.edu.in'),
            ('Prof. Bharti Jain', 'M.Sc in Biology', 'Assistant Professor', '6 years', 'bharti.jain@mitwpu.edu.in'),
            ('Dr. Dinesh Kumar', 'PhD in Environmental Science', 'Professor', '17 years', 'dinesh.kumar@mitwpu.edu.in'),
            ('Prof. Sudha Agrawal', 'M.Sc in Statistics', 'Associate Professor', '9 years', 'sudha.agrawal@mitwpu.edu.in'),
            
            # Design Faculty
            ('Prof. Nitin Bhatt', 'M.Des in Product Design', 'Associate Professor', '11 years', 'nitin.bhatt@mitwpu.edu.in'),
            ('Dr. Asha Kulkarni', 'PhD in Design', 'Professor', '15 years', 'asha.kulkarni@mitwpu.edu.in'),
            ('Prof. Rohit Thakur', 'M.Des in Fashion', 'Assistant Professor', '7 years', 'rohit.thakur@mitwpu.edu.in'),
            ('Prof. Maya Devi', 'M.Des in Interior Design', 'Associate Professor', '10 years', 'maya.devi@mitwpu.edu.in'),
            ('Dr. Tarun Jha', 'PhD in Visual Arts', 'Professor', '13 years', 'tarun.jha@mitwpu.edu.in'),
            
            # Liberal Arts Faculty
            ('Dr. Seema Bose', 'PhD in English Literature', 'Professor', '18 years', 'seema.bose@mitwpu.edu.in'),
            ('Prof. Ajay Ghosh', 'MA in Psychology', 'Associate Professor', '12 years', 'ajay.ghosh@mitwpu.edu.in'),
            ('Dr. Ritu Roy', 'PhD in Political Science', 'Professor', '16 years', 'ritu.roy@mitwpu.edu.in'),
            ('Prof. Sanjeev Chatterjee', 'MA in Media Studies', 'Assistant Professor', '8 years', 'sanjeev.chatterjee@mitwpu.edu.in'),
            ('Dr. Nandini Sen', 'PhD in Education', 'Professor', '20 years', 'nandini.sen@mitwpu.edu.in'),
            
            # Law Faculty
            ('Dr. Aditya Sharma', 'LL.M, PhD in Law', 'Professor', '19 years', 'aditya.sharma@mitwpu.edu.in'),
            ('Prof. Kaveri Patel', 'LL.M in Corporate Law', 'Associate Professor', '11 years', 'kaveri.patel@mitwpu.edu.in'),
            ('Dr. Harsh Gupta', 'LL.M in Criminal Law', 'Professor', '15 years', 'harsh.gupta@mitwpu.edu.in'),
            ('Prof. Smita Reddy', 'LL.M in Constitutional Law', 'Assistant Professor', '9 years', 'smita.reddy@mitwpu.edu.in'),
            
            # Leadership & Government Faculty
            ('Dr. Mahesh Singh', 'PhD in Public Administration', 'Professor', '22 years', 'mahesh.singh@mitwpu.edu.in'),
            ('Prof. Vandana Jain', 'MA in Political Leadership', 'Associate Professor', '13 years', 'vandana.jain@mitwpu.edu.in'),
            ('Dr. Rajiv Kumar', 'PhD in Government Studies', 'Professor', '17 years', 'rajiv.kumar@mitwpu.edu.in'),
            
            # Consciousness Studies Faculty
            ('Dr. Swami Anandananda', 'PhD in Philosophy', 'Professor', '25 years', 'swami.anandananda@mitwpu.edu.in'),
            ('Prof. Medha Sharma', 'MA in Consciousness Studies', 'Associate Professor', '10 years', 'medha.sharma@mitwpu.edu.in'),
        ]
        
        # Create teacher users and profiles
        teachers_created = 0
        teacher_objects = []
        
        # Get existing teachers first
        existing_teachers = list(Teacher.objects.all())
        teacher_objects.extend(existing_teachers)
        
        for name, qualification, designation, experience, email in teacher_data:
            # Create username from name
            username = name.lower().replace('dr. ', '').replace('prof. ', '').replace(' ', '_')
            
            # Split name for first and last name
            name_parts = name.replace('Dr. ', '').replace('Prof. ', '').split()
            first_name = name_parts[0]
            last_name = ' '.join(name_parts[1:])
            
            # Create teacher user
            user, user_created = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'user_type': 'teacher'
                }
            )
            
            if user_created:
                user.set_password('teacher123')
                user.save()
                
                # Create teacher profile
                teacher, teacher_created = Teacher.objects.get_or_create(
                    user=user,
                    defaults={
                        'employee_id': f'T{str(len(teacher_objects) + teachers_created + 1001).zfill(4)}',
                        'department': random.choice(Department.objects.all()),
                        'designation': designation,
                        'qualification': 'phd' if 'PhD' in qualification else 'master',
                        'specialization': qualification,
                        'experience_years': int(experience.split()[0]) if experience.split()[0].isdigit() else 5,
                        'employment_type': 'permanent',
                        'joining_date': date(random.randint(2010, 2023), random.randint(1, 12), random.randint(1, 28)),
                        'salary': random.randint(50000, 120000),
                        'office_room': f'Room-{random.randint(200, 300)}',
                        'office_hours': '9:00 AM - 5:00 PM',
                        'research_interests': f'Research in {qualification}',
                        'is_active': True,
                    }
                )
                
                if teacher_created:
                    teacher_objects.append(teacher)
                    teachers_created += 1
            else:
                # User exists, check if teacher profile exists
                try:
                    existing_teacher = Teacher.objects.get(user=user)
                    if existing_teacher not in teacher_objects:
                        teacher_objects.append(existing_teacher)
                except Teacher.DoesNotExist:
                    pass
        
        self.stdout.write(f'👨‍🏫 Teachers: {teachers_created} created with detailed profiles')
        
        # Create subjects for each course with assigned teachers
        subjects_created = 0
        all_courses = Course.objects.all()
        all_classes = Class.objects.all()
        
        # Subject templates based on course types
        subject_patterns = {
            # Engineering subjects
            'engineering': [
                'Theory', 'Laboratory', 'Workshop', 'Project Work', 'Seminar'
            ],
            # Computer Science subjects  
            'computer': [
                'Theory', 'Programming Lab', 'Project', 'Seminar', 'Industrial Training'
            ],
            # Business subjects
            'business': [
                'Theory', 'Case Study', 'Project', 'Internship', 'Presentation'
            ],
            # Science subjects
            'science': [
                'Theory', 'Practical', 'Research Project', 'Field Work', 'Dissertation'
            ],
            # Arts subjects
            'arts': [
                'Theory', 'Tutorial', 'Research', 'Creative Work', 'Thesis'
            ],
            # Default pattern
            'default': [
                'Theory', 'Practical', 'Project', 'Assignment', 'Evaluation'
            ]
        }
        
        for course in all_courses:
            # Determine subject pattern based on course name/department
            pattern_key = 'default'
            course_name_lower = course.name.lower()
            
            if any(word in course_name_lower for word in ['engineering', 'mechanical', 'civil', 'chemical', 'electrical']):
                pattern_key = 'engineering'
            elif any(word in course_name_lower for word in ['computer', 'programming', 'software', 'data', 'ai']):
                pattern_key = 'computer'
            elif any(word in course_name_lower for word in ['business', 'management', 'mba', 'marketing', 'finance']):
                pattern_key = 'business'
            elif any(word in course_name_lower for word in ['physics', 'chemistry', 'biology', 'science', 'mathematics']):
                pattern_key = 'science'
            elif any(word in course_name_lower for word in ['arts', 'literature', 'psychology', 'english', 'media']):
                pattern_key = 'arts'
            
            # Create 3-5 subjects per course
            subject_types = subject_patterns[pattern_key]
            num_subjects = random.randint(3, min(5, len(subject_types)))
            selected_types = random.sample(subject_types, num_subjects)
            
            # Get relevant classes for this course's department
            course_classes = [cls for cls in all_classes if cls.department == course.department]
            
            for subject_type in selected_types:
                subject_name = f'{course.name} - {subject_type}'
                
                # Assign random teacher (preferably from same or related department)
                suitable_teachers = [t for t in teacher_objects if t.department == course.department]
                if not suitable_teachers:
                    suitable_teachers = teacher_objects
                
                assigned_teacher = random.choice(suitable_teachers)
                
                # Create subject for each relevant class
                for class_obj in course_classes[:3]:  # Limit to 3 classes per subject to avoid too much data
                    subject, created = Subject.objects.get_or_create(
                        course=course,
                        class_assigned=class_obj,
                        defaults={
                            'teacher': assigned_teacher.user,
                        }
                    )
                    
                    if created:
                        subjects_created += 1
        
        self.stdout.write(f'📖 Subjects: {subjects_created} created with teacher assignments')
        
        # Assign HODs to departments
        self.stdout.write('Assigning Head of Departments (HODs)...')
        
        hods_assigned = 0
        departments_without_hod = Department.objects.filter(head__isnull=True)
        
        # Define preferred HOD assignments based on seniority and expertise
        preferred_hods = {
            'SET': 'Dr. Amit Patel',  # Chemical Engineering with 18 years experience
            'SCSE': 'Dr. Rahul Mehta',  # Computer Science with 16 years experience
            'SOB': 'Dr. Sanjay Khanna',  # Business Administration with 20 years experience
            'SEC': 'Dr. Vijay Saxena',  # Economics with 19 years experience
            'SHST': 'Dr. Sunil Rao',  # Pharmacy with 18 years experience
            'SSES': 'Dr. Mohan Das',  # Physics with 21 years experience
            'SOD': 'Dr. Asha Kulkarni',  # Design with 15 years experience
            'SLA': 'Dr. Seema Bose',  # English Literature with 18 years experience
            'SOL': 'Dr. Aditya Sharma',  # Law with 19 years experience
            'SOG': 'Dr. Mahesh Singh',  # Public Administration with 22 years experience
            'RSL': 'Dr. Rajiv Kumar',  # Government Studies with 17 years experience
            'SOC': 'Dr. Swami Anandananda',  # Philosophy with 25 years experience
        }
        
        for dept in departments_without_hod:
            dept_code = dept.code
            
            if dept_code in preferred_hods:
                # Try to find the preferred HOD
                preferred_name = preferred_hods[dept_code]
                username = preferred_name.lower().replace('dr. ', '').replace('prof. ', '').replace(' ', '_')
                
                try:
                    hod_user = User.objects.get(username=username)
                    # Verify the user is a teacher and not already an HOD
                    if (hod_user.user_type == 'teacher' and 
                        not Department.objects.filter(head=hod_user).exists()):
                        
                        dept.head = hod_user
                        dept.save()
                        hods_assigned += 1
                        self.stdout.write(f'  🔹 {dept.name}: {preferred_name} appointed as HOD')
                        continue
                except User.DoesNotExist:
                    pass
            
            # If preferred HOD not found, assign senior teacher from same department
            dept_teachers = Teacher.objects.filter(department=dept).order_by('-experience_years')
            
            # Try to find a Professor first, then Associate Professor
            for designation in ['Professor', 'Associate Professor', 'Assistant Professor']:
                suitable_teachers = dept_teachers.filter(designation=designation)
                
                for teacher in suitable_teachers:
                    # Check if teacher is not already an HOD
                    if not Department.objects.filter(head=teacher.user).exists():
                        dept.head = teacher.user
                        dept.save()
                        hods_assigned += 1
                        self.stdout.write(f'  🔹 {dept.name}: {teacher.user.get_full_name()} appointed as HOD')
                        break
                
                if dept.head:  # If HOD assigned, break the designation loop
                    break
            
            # If no teacher from same department, assign any senior teacher
            if not dept.head:
                all_senior_teachers = Teacher.objects.filter(
                    designation='Professor',
                    experience_years__gte=10
                ).exclude(
                    user__in=Department.objects.filter(head__isnull=False).values('head')
                ).order_by('-experience_years')
                
                if all_senior_teachers:
                    senior_teacher = all_senior_teachers.first()
                    dept.head = senior_teacher.user
                    dept.save()
                    hods_assigned += 1
                    self.stdout.write(f'  🔹 {dept.name}: {senior_teacher.user.get_full_name()} appointed as HOD (cross-department)')
        
        self.stdout.write(f'🏛️ HODs: {hods_assigned} Head of Departments assigned')
        
        # Create additional teacher privileges for HODs
        self.create_hod_privileges()
        
        # Create time slots
        time_slots_data = [
            ('monday', '09:00', '10:00'),
            ('monday', '10:00', '11:00'),
            ('tuesday', '09:00', '10:00'),
            ('tuesday', '10:00', '11:00'),
            ('wednesday', '09:00', '10:00'),
            ('wednesday', '10:00', '11:00'),
            ('thursday', '09:00', '10:00'),
            ('thursday', '10:00', '11:00'),
            ('friday', '09:00', '10:00'),
            ('friday', '10:00', '11:00'),
        ]
        
        for day, start_time, end_time in time_slots_data:
            TimeSlot.objects.get_or_create(
                day=day,
                start_time=start_time,
                end_time=end_time
            )
        
        # Get all subjects for timetable creation
        all_subjects = Subject.objects.all()[:20]  # Limit for initial timetable
        
        # Create timetable
        time_slots = TimeSlot.objects.all()[:len(all_subjects)]
        for subject, time_slot in zip(all_subjects, time_slots):
            # Get a random class for timetable assignment
            random_class = random.choice(Class.objects.all())
            Timetable.objects.get_or_create(
                class_assigned=random_class,
                subject=subject,
                time_slot=time_slot,
                defaults={'room_number': f'Room-{random.randint(100, 200)}'}
            )
        
        # Create attendance records for the past 30 days
        sample_students = Student.objects.all()[:100]  # Sample students for attendance
        start_date = timezone.now().date() - timedelta(days=30)
        
        for i in range(30):
            current_date = start_date + timedelta(days=i)
            if current_date.weekday() < 5:  # Only weekdays
                sample_subjects = Subject.objects.all()[:10]  # Sample subjects
                for subject in sample_subjects:
                    for student_obj in sample_students[:20]:  # Limit students per subject
                        # 85% attendance rate
                        is_present = random.random() < 0.85
                        teacher_for_marking = subject.teacher
                        Attendance.objects.get_or_create(
                            student=student_obj.user,
                            subject=subject,
                            date=current_date,
                            defaults={
                                'is_present': is_present,
                                'marked_by': teacher_for_marking
                            }
                        )
        
        # Create exams
        exam_data = [
            ('Mid-term Exam - Programming', 'midterm', 0),
            ('Quiz - Data Structures', 'quiz', 5),
            ('Final Exam - Mathematics', 'final', 10),
            ('Assignment - Physics', 'assignment', 15),
            ('Project - English', 'project', 20),
        ]
        
        sample_subjects_for_exam = Subject.objects.all()[:10]  # Sample subjects for exams
        sample_students_for_exam = Student.objects.all()[:50]  # Sample students for results
        
        for exam_name, exam_type, days_from_now in exam_data:
            exam_date = timezone.now() + timedelta(days=days_from_now)
            if sample_subjects_for_exam:
                subject = random.choice(sample_subjects_for_exam)
                teacher_for_exam = subject.teacher
                
                exam, created = Exam.objects.get_or_create(
                    name=exam_name,
                    subject=subject,
                    defaults={
                        'exam_type': exam_type,
                        'date': exam_date,
                        'duration': timedelta(hours=2),
                        'total_marks': 100,
                        'pass_marks': 40,
                        'instructions': f'Instructions for {exam_name}',
                        'created_by': teacher_for_exam
                    }
                )
                
                # Create results for past exams
                if days_from_now <= 0:
                    for student_obj in sample_students_for_exam:
                        marks = random.randint(30, 95)
                        Result.objects.get_or_create(
                            student=student_obj.user,
                            exam=exam,
                            defaults={
                                'marks_obtained': marks,
                                'is_published': True
                            }
                        )
        
        # Create fees
        fee_types = ['tuition', 'library', 'lab', 'exam', 'development']
        amounts = [15000, 500, 1000, 300, 2000]
        
        sample_students_for_fees = Student.objects.all()[:100]  # Sample students for fees
        
        for student_obj in sample_students_for_fees:
            for fee_type, amount in zip(fee_types, amounts):
                # Some fees paid, some pending
                is_paid = random.random() < 0.7
                due_date = date(2024, 12, 31)
                
                fee_obj = Fee.objects.get_or_create(
                    student=student_obj.user,
                    fee_type=fee_type,
                    academic_year='2024-2025',
                    semester=1,
                    defaults={
                        'amount': amount,
                        'due_date': due_date,
                        'payment_status': 'paid' if is_paid else 'pending'
                    }
                )[0]
                
                if is_paid:
                    fee_obj.payment_date = date(2024, random.randint(8, 11), random.randint(1, 28))
                    fee_obj.payment_method = 'Online'
                    fee_obj.transaction_id = f'TXN{random.randint(100000, 999999)}'
                    fee_obj.save()
        
        # Create notifications
        notifications_data = [
            ('Welcome to New Academic Year', 'Academic year 2024-2025 has begun. Wishing all students success!', 'academic'),
            ('Library Hours Extended', 'Library will remain open until 10 PM during exam season.', 'general'),
            ('Sports Day Announcement', 'Annual sports day scheduled for next month. Registration open!', 'event'),
            ('Fee Payment Reminder', 'Please clear your pending fees by the due date to avoid late charges.', 'fee'),
            ('Mid-term Exam Schedule', 'Mid-term examinations will commence from next week. Check your timetable.', 'exam'),
        ]
        
        # Get a teacher for notifications
        notification_teacher = User.objects.filter(user_type='teacher').first()
        if not notification_teacher:
            # Create a default admin user for notifications if no teacher exists
            notification_teacher = User.objects.filter(is_staff=True).first()
        
        for title, message, notif_type in notifications_data:
            Notification.objects.get_or_create(
                title=title,
                defaults={
                    'message': message,
                    'notification_type': notif_type,
                    'target_audience': 'all',
                    'is_urgent': notif_type == 'exam',
                    'created_by': notification_teacher
                }
            )
        
        self.stdout.write(
            self.style.SUCCESS('🎉 Enhanced sample data with MIT-WPU departments created successfully!')
        )
        self.stdout.write('📊 Enhanced data includes:')
        self.stdout.write('  🏫 12 MIT-WPU Schools/Departments with detailed descriptions')
        self.stdout.write('  📚 Multiple courses for each major department')
        self.stdout.write('  🏛️ Classes for all major departments (2023-24 & 2024-25)')
        self.stdout.write('  👥 10 students with complete profiles')
        self.stdout.write('  📖 5 subjects with timetable')
        self.stdout.write('  📅 30 days of attendance records')
        self.stdout.write('  📝 5 exams with results')
        self.stdout.write('  💰 Fee records for all students')
        self.stdout.write('  📢 5 system notifications')
        self.stdout.write('')
        self.stdout.write('🏫 All MIT-WPU Schools added:')
        for dept in Department.objects.all().order_by('code'):
            self.stdout.write(f'  • {dept.code}: {dept.name}')
        self.stdout.write('')
        self.stdout.write('✨ Your College ERP now supports the complete MIT-WPU structure!')
        self.stdout.write('💡 Access the admin dashboard to see updated department statistics.')