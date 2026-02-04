"""
Database Seeder - Creates sample data for LearnHub
Usage: python manage.py seed
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import (
    Course, Module, Enrollment, Assessment, Question, Choice,
    AssessmentResult, Certificate, Commission, CommissionRate
)
from decimal import Decimal
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed database with sample data (clears existing data first)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--no-clear',
            action='store_true',
            help='Do not clear existing data before seeding',
        )

    def handle(self, *args, **options):
        if not options['no_clear']:
            self.stdout.write(self.style.WARNING('🗑️  Clearing existing data...'))
            self.clear_data()
        
        self.stdout.write(self.style.SUCCESS('🌱 Seeding database...'))
        
        # Create users
        users = self.create_users()
        self.stdout.write(f'   ✓ Created {len(users)} users')
        
        # Create courses
        courses = self.create_courses(users['mentors'])
        self.stdout.write(f'   ✓ Created {len(courses)} courses')
        
        # Create modules for each course
        total_modules = self.create_modules(courses)
        self.stdout.write(f'   ✓ Created {total_modules} modules')
        
        # Create assessments
        assessments = self.create_assessments(courses)
        self.stdout.write(f'   ✓ Created {len(assessments)} assessments with questions')
        
        # Create enrollments
        enrollments = self.create_enrollments(users['students'], courses)
        self.stdout.write(f'   ✓ Created {len(enrollments)} enrollments')
        
        # Create commission rates
        rates = self.create_commission_rates(courses)
        self.stdout.write(f'   ✓ Created {len(rates)} commission rates')
        
        # Create some assessment results and certificates
        results = self.create_assessment_results(enrollments, assessments)
        self.stdout.write(f'   ✓ Created {len(results)} assessment results')
        
        certs = self.create_certificates(enrollments)
        self.stdout.write(f'   ✓ Created {len(certs)} certificates')
        
        # Create commissions
        commissions = self.create_commissions(users, enrollments)
        self.stdout.write(f'   ✓ Created {len(commissions)} commissions')
        
        self.stdout.write(self.style.SUCCESS('\n✅ Database seeded successfully!'))
        self.stdout.write(self.style.SUCCESS('\n📋 Summary:'))
        self.stdout.write(f'   • Admin: admin / admin123')
        self.stdout.write(f'   • Owner: owner / owner123')
        self.stdout.write(f'   • Mentors: mentor1, mentor2, mentor3 / password123')
        self.stdout.write(f'   • Students: student1-5 / password123')

    def clear_data(self):
        """Clear all data except superusers"""
        Commission.objects.all().delete()
        CommissionRate.objects.all().delete()
        Certificate.objects.all().delete()
        AssessmentResult.objects.all().delete()
        Choice.objects.all().delete()
        Question.objects.all().delete()
        Assessment.objects.all().delete()
        Enrollment.objects.all().delete()
        Module.objects.all().delete()
        Course.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()

    def create_users(self):
        """Create sample users with different roles"""
        users = {'admin': None, 'owner': None, 'mentors': [], 'students': []}
        
        # Admin (keep existing or create new)
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@learnhub.local',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
                'email_verified': True,
                'profile_completed': True,
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
        users['admin'] = admin
        
        # Owner
        owner, created = User.objects.get_or_create(
            username='owner',
            defaults={
                'email': 'owner@learnhub.local',
                'role': 'owner',
                'is_staff': True,
                'email_verified': True,
                'profile_completed': True,
            }
        )
        if created:
            owner.set_password('owner123')
            owner.save()
        users['owner'] = owner
        
        # Mentors (Penulis)
        mentor_data = [
            {'username': 'mentor1', 'first_name': 'Budi', 'last_name': 'Santoso', 'bank': '1234567890'},
            {'username': 'mentor2', 'first_name': 'Siti', 'last_name': 'Rahayu', 'bank': '0987654321'},
            {'username': 'mentor3', 'first_name': 'Ahmad', 'last_name': 'Wijaya', 'bank': '1122334455'},
        ]
        
        for data in mentor_data:
            mentor, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'email': f"{data['username']}@learnhub.local",
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'role': 'penulis',
                    'is_mentor': True,
                    'email_verified': True,
                    'profile_completed': True,
                    'bank_account_number': data['bank'],
                    'phone': f"08123456789{len(users['mentors'])}",
                }
            )
            if created:
                mentor.set_password('password123')
                mentor.save()
            users['mentors'].append(mentor)
        
        # Students (Pembaca)
        for i in range(1, 6):
            student, created = User.objects.get_or_create(
                username=f'student{i}',
                defaults={
                    'email': f'student{i}@learnhub.local',
                    'first_name': f'Student',
                    'last_name': f'{i}',
                    'role': 'pembaca',
                    'email_verified': True,
                    'profile_completed': True,
                    'phone': f'0812000000{i}',
                }
            )
            if created:
                student.set_password('password123')
                student.save()
            users['students'].append(student)
        
        return users

    def create_courses(self, mentors):
        """Create sample courses"""
        courses_data = [
            {
                'title': 'Python untuk Pemula',
                'description': 'Belajar bahasa pemrograman Python dari dasar. Cocok untuk pemula yang ingin memulai karir di bidang programming.',
                'price': Decimal('150000'),
                'level': 'beginner',
                'duration_hours': 20,
            },
            {
                'title': 'Web Development dengan Django',
                'description': 'Pelajari cara membangun aplikasi web modern dengan framework Django. Termasuk REST API dan deployment.',
                'price': Decimal('350000'),
                'level': 'intermediate',
                'duration_hours': 40,
            },
            {
                'title': 'JavaScript Modern (ES6+)',
                'description': 'Kuasai JavaScript modern dengan fitur ES6+. Arrow functions, promises, async/await, dan banyak lagi.',
                'price': Decimal('200000'),
                'level': 'intermediate',
                'duration_hours': 25,
            },
            {
                'title': 'React.js Fundamental',
                'description': 'Belajar React.js dari nol hingga mahir. Termasuk hooks, state management, dan best practices.',
                'price': Decimal('400000'),
                'level': 'intermediate',
                'duration_hours': 35,
            },
            {
                'title': 'Data Science dengan Python',
                'description': 'Analisis data dan machine learning menggunakan Python, Pandas, NumPy, dan Scikit-learn.',
                'price': Decimal('500000'),
                'level': 'advanced',
                'duration_hours': 50,
            },
            {
                'title': 'Database MySQL Lengkap',
                'description': 'Pelajari MySQL dari dasar sampai advanced. Query, optimization, stored procedures, dan design database.',
                'price': Decimal('250000'),
                'level': 'beginner',
                'duration_hours': 30,
            },
        ]
        
        courses = []
        for i, data in enumerate(courses_data):
            mentor = mentors[i % len(mentors)]
            course = Course.objects.create(
                mentor=mentor,
                **data
            )
            courses.append(course)
        
        return courses

    def create_modules(self, courses):
        """Create modules for each course"""
        total = 0
        
        module_templates = {
            'Python untuk Pemula': [
                ('Pengenalan Python', 'text', 'Python adalah bahasa pemrograman yang mudah dipelajari dan sangat powerful...'),
                ('Instalasi Python', 'video', 'https://youtube.com/watch?v=example1'),
                ('Variabel dan Tipe Data', 'text', 'Variabel adalah wadah untuk menyimpan data...'),
                ('Operator di Python', 'code', 'Praktik menggunakan operator aritmatika dan logika'),
                ('Kontrol Alur (If-Else)', 'text', 'Percabangan memungkinkan program mengambil keputusan...'),
                ('Perulangan (Loop)', 'code', 'Praktik menggunakan for dan while loop'),
            ],
            'Web Development dengan Django': [
                ('Pengenalan Django', 'text', 'Django adalah framework web Python yang powerful...'),
                ('Setup Project Django', 'video', 'https://youtube.com/watch?v=example2'),
                ('Models dan Database', 'text', 'Django ORM memudahkan interaksi dengan database...'),
                ('Views dan Templates', 'code', 'Membuat halaman web dinamis'),
                ('Forms dan Validasi', 'text', 'Handling form submission dengan Django...'),
                ('REST API dengan DRF', 'code', 'Membuat API dengan Django REST Framework'),
            ],
        }
        
        for course in courses:
            templates = module_templates.get(course.title, [
                ('Pendahuluan', 'text', f'Selamat datang di kursus {course.title}...'),
                ('Materi Dasar', 'video', 'https://youtube.com/watch?v=example'),
                ('Latihan 1', 'code', 'Praktik pertama'),
                ('Materi Lanjutan', 'text', 'Pembahasan materi lanjutan...'),
                ('Latihan 2', 'code', 'Praktik kedua'),
                ('Penutup', 'text', 'Rangkuman dan kesimpulan...'),
            ])
            
            for order, (title, content_type, content) in enumerate(templates, 1):
                Module.objects.create(
                    course=course,
                    title=title,
                    order=order,
                    content_type=content_type,
                    content=content,
                    video_url=content if content_type == 'video' else '',
                    language='python',
                    starter_code='# Write your code here\n' if content_type == 'code' else '',
                    expected_output='Success!' if content_type == 'code' else '',
                )
                total += 1
        
        return total

    def create_assessments(self, courses):
        """Create assessments with questions for each course"""
        assessments = []
        
        questions_template = [
            {
                'text': 'Apa output dari kode berikut: print(2 + 2)?',
                'choices': [('4', True), ('22', False), ('Error', False), ('None', False)],
            },
            {
                'text': 'Manakah yang merupakan tipe data di Python?',
                'choices': [('int', True), ('number', False), ('digit', False), ('num', False)],
            },
            {
                'text': 'Bagaimana cara membuat komentar di Python?',
                'choices': [('# ini komentar', True), ('// ini komentar', False), ('/* komentar */', False), ('-- komentar', False)],
            },
            {
                'text': 'Apa fungsi dari keyword "def"?',
                'choices': [('Mendefinisikan fungsi', True), ('Mendefinisikan variabel', False), ('Import module', False), ('Membuat class', False)],
            },
            {
                'text': 'Bagaimana cara mengakses elemen pertama dari list?',
                'choices': [('list[0]', True), ('list[1]', False), ('list.first()', False), ('list.get(0)', False)],
            },
        ]
        
        for course in courses:
            assessment = Assessment.objects.create(
                course=course,
                title=f'Assessment: {course.title}',
                passing_score=70,
            )
            
            for order, q_data in enumerate(questions_template, 1):
                question = Question.objects.create(
                    assessment=assessment,
                    text=q_data['text'],
                    order=order,
                )
                
                for choice_text, is_correct in q_data['choices']:
                    Choice.objects.create(
                        question=question,
                        text=choice_text,
                        is_correct=is_correct,
                    )
            
            assessments.append(assessment)
        
        return assessments

    def create_enrollments(self, students, courses):
        """Create enrollments for students"""
        enrollments = []
        
        for student in students:
            # Each student enrolls in 2-4 random courses
            num_courses = random.randint(2, min(4, len(courses)))
            selected_courses = random.sample(courses, num_courses)
            
            for course in selected_courses:
                # Random progress
                all_modules = list(course.modules.values_list('id', flat=True))
                completed = random.sample(all_modules, random.randint(0, len(all_modules)))
                
                enrollment = Enrollment.objects.create(
                    user=student,
                    course=course,
                    payment_status='completed',
                    progress={'completed_modules': completed},
                    completed=len(completed) == len(all_modules),
                )
                enrollments.append(enrollment)
        
        return enrollments

    def create_commission_rates(self, courses):
        """Create commission rates"""
        rates = []
        
        # Global rates
        for role in ['penulis', 'admin', 'layanan']:
            percentage = {'penulis': 60, 'admin': 10, 'layanan': 30}[role]
            rate, _ = CommissionRate.objects.get_or_create(
                role=role,
                course=None,
                defaults={
                    'rate_type': 'percentage',
                    'percentage': Decimal(percentage),
                    'is_active': True,
                }
            )
            rates.append(rate)
        
        return rates

    def create_assessment_results(self, enrollments, assessments):
        """Create assessment results for completed enrollments"""
        results = []
        
        for enrollment in enrollments:
            if enrollment.completed:
                try:
                    assessment = Assessment.objects.get(course=enrollment.course)
                    score = random.randint(60, 100)
                    result = AssessmentResult.objects.create(
                        user=enrollment.user,
                        assessment=assessment,
                        enrollment=enrollment,
                        score=score,
                        answers={},
                        passed=score >= assessment.passing_score,
                    )
                    results.append(result)
                except Assessment.DoesNotExist:
                    pass
        
        return results

    def create_certificates(self, enrollments):
        """Create certificates for completed enrollments with passing scores"""
        certs = []
        
        for enrollment in enrollments:
            if enrollment.completed:
                try:
                    result = AssessmentResult.objects.get(enrollment=enrollment)
                    if result.passed:
                        cert = Certificate.objects.create(
                            user=enrollment.user,
                            course=enrollment.course,
                            enrollment=enrollment,
                        )
                        certs.append(cert)
                except AssessmentResult.DoesNotExist:
                    pass
        
        return certs

    def create_commissions(self, users, enrollments):
        """Create commission records"""
        commissions = []
        
        for enrollment in enrollments:
            if enrollment.payment_status == 'completed':
                course = enrollment.course
                price = course.price
                
                # Penulis commission (60%)
                if course.mentor:
                    comm = Commission.objects.create(
                        user=course.mentor,
                        role='penulis',
                        enrollment=enrollment,
                        course=course,
                        amount=price * Decimal('0.60'),
                        rate_type='percentage',
                        rate_value=Decimal('60'),
                        status=random.choice(['pending', 'paid']),
                    )
                    commissions.append(comm)
                
                # Admin commission (10%)
                if users.get('admin'):
                    comm = Commission.objects.create(
                        user=users['admin'],
                        role='admin',
                        enrollment=enrollment,
                        course=course,
                        amount=price * Decimal('0.10'),
                        rate_type='percentage',
                        rate_value=Decimal('10'),
                        status='pending',
                    )
                    commissions.append(comm)
        
        return commissions
