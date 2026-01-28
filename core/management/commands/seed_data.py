from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Course, Module, Enrollment, Assessment, Question, Choice
from decimal import Decimal
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # 1. Create Users
        self.stdout.write('Creating users...')

        # Admin
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()

        # Owner
        owner_user, created = User.objects.get_or_create(
            username='owner',
            defaults={
                'email': 'owner@example.com',
                'role': 'owner',
            }
        )
        if created:
            owner_user.set_password('owner123')
            owner_user.save()

        # Mentors (Penulis)
        mentors = []
        for i in range(1, 4):
            mentor, created = User.objects.get_or_create(
                username=f'mentor{i}',
                defaults={
                    'email': f'mentor{i}@example.com',
                    'role': 'penulis',
                    'is_mentor': True,
                }
            )
            if created:
                mentor.set_password('mentor123')
                mentor.save()
            mentors.append(mentor)

        # Students (Pembaca)
        students = []
        for i in range(1, 6):
            student, created = User.objects.get_or_create(
                username=f'student{i}',
                defaults={
                    'email': f'student{i}@example.com',
                    'role': 'pembaca',
                }
            )
            if created:
                student.set_password('student123')
                student.save()
            students.append(student)

        # 2. Create Courses
        self.stdout.write('Creating courses...')
        courses = []
        course_titles = [
            ('Python for Beginners', 'Learn the basics of Python programming.', 'beginner', 20, 150000),
            ('Advanced Django', 'Master Django web framework.', 'advanced', 40, 350000),
            ('Data Science with Python', 'Analyze data using Pandas and NumPy.', 'intermediate', 30, 250000),
            ('Web Development with React', 'Build modern web apps with React.', 'intermediate', 25, 200000),
        ]

        for title, desc, level, duration, price in course_titles:
            course, created = Course.objects.get_or_create(
                title=title,
                defaults={
                    'description': desc,
                    'level': level,
                    'duration_hours': duration,
                    'price': Decimal(str(price)),
                    'mentor': random.choice(mentors),
                    'is_active': True,
                }
            )
            courses.append(course)

        # 3. Create Modules
        self.stdout.write('Creating modules...')
        for course in courses:
            for i in range(1, 6):
                Module.objects.get_or_create(
                    course=course,
                    title=f'Module {i}: Introduction to {course.title}',
                    defaults={
                        'content': f'# Welcome to Module {i}\n\nThis is the content for module {i} of {course.title}.',
                        'content_type': 'text',
                        'order': i,
                    }
                )

        # 5. Create Assessments
        self.stdout.write('Creating assessments...')
        for course in courses:
            assessment, created = Assessment.objects.get_or_create(
                course=course,
                defaults={
                    'title': f'Final Assessment for {course.title}',
                    'passing_score': 70,
                }
            )
            
            if created:
                # Add 3 sample questions for each assessment
                for i in range(1, 4):
                    question = Question.objects.create(
                        assessment=assessment,
                        text=f'Question {i}: What is the primary focus of {course.title}?',
                        order=i
                    )
                    
                    # Add 4 choices for each question
                    Choice.objects.create(question=question, text='Option A (Correct)', is_correct=True)
                    Choice.objects.create(question=question, text='Option B', is_correct=False)
                    Choice.objects.create(question=question, text='Option C', is_correct=False)
                    Choice.objects.create(question=question, text='Option D', is_correct=False)

        self.stdout.write(self.style.SUCCESS('Successfully seeded database!'))
