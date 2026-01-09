"""
Management command to create sample course data for testing
Usage: python manage.py seed_data
"""

from django.core.management.base import BaseCommand
from core.models import Course, Module, Assessment


class Command(BaseCommand):
    help = 'Seeds database with sample course data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        # Create sample course
        course, created = Course.objects.get_or_create(
            title='Python Programming Fundamentals',
            defaults={
                'description': 'Learn Python programming from scratch. This comprehensive course covers variables, data types, control structures, functions, and object-oriented programming. Perfect for beginners who want to start their programming journey.',
                'price': 49.99,
                'level': 'beginner',
                'duration_hours': 12,
                'is_active': True
            }
        )

        if created:
            self.stdout.write(self.stdout.SUCCESS('Created course: Python Programming Fundamentals'))

            # Create modules
            modules = [
                {
                    'title': 'Introduction to Python',
                    'order': 1,
                    'content_type': 'text',
                    'content': '''Welcome to Python Programming!

Python is a powerful, easy-to-learn programming language. It has efficient high-level data structures and a simple but effective approach to object-oriented programming.

In this course, you will learn:
- Variables and data types
- Control structures (if, while, for)
- Functions and modules
- Object-oriented programming basics
- File handling and error handling

Let's get started!'''
                },
                {
                    'title': 'Your First Python Program',
                    'order': 2,
                    'content_type': 'code',
                    'content': 'Write a Python program that prints "Hello, World!" to the console.',
                    'starter_code': '# Write your code here\nprint("Hello, World!")',
                    'expected_output': 'Hello, World!\n'
                },
                {
                    'title': 'Variables and Data Types',
                    'order': 3,
                    'content_type': 'text',
                    'content': '''Variables in Python

A variable is a container for storing data values. Python has no command for declaring a variable; it is created the moment you first assign a value to it.

Example:
x = 5
name = "John"
is_valid = True

Python has the following built-in data types:
- Text: str
- Numeric: int, float, complex
- Sequence: list, tuple, range
- Boolean: bool
- None: NoneType'''
                },
                {
                    'title': 'Working with Variables',
                    'order': 4,
                    'content_type': 'code',
                    'content': 'Create variables for your name, age, and favorite number, then print them.',
                    'starter_code': '# Create and print variables\nname = "Your Name"\nage = 25\nfavorite_number = 7\n\nprint(f"My name is {name}")\nprint(f"I am {age} years old")\nprint(f"My favorite number is {favorite_number}")'
                },
                {
                    'title': 'Python Tutorial Video',
                    'order': 5,
                    'content_type': 'video',
                    'content': 'Watch this video to learn more about Python basics.',
                    'video_url': 'https://www.youtube.com/embed/rfscVS0vtbw'
                },
                {
                    'title': 'Conditional Statements',
                    'order': 6,
                    'content_type': 'code',
                    'content': 'Write a program that checks if a number is positive, negative, or zero.',
                    'starter_code': '# Check if a number is positive, negative, or zero\nnumber = 10\n\nif number > 0:\n    print("Positive")\nelif number < 0:\n    print("Negative")\nelse:\n    print("Zero")'
                },
                {
                    'title': 'Summary and Next Steps',
                    'order': 7,
                    'content_type': 'text',
                    'content': '''Congratulations!

You have completed the Python Programming Fundamentals module. You should now understand:
- How to write basic Python programs
- Variables and data types
- Control structures
- How to use the interactive compiler

Next, take the assessment to earn your certificate!

Keep practicing and happy coding!'''
                }
            ]

            for module_data in modules:
                module_data['course'] = course
                Module.objects.create(**module_data)
                self.stdout.write(f'Created module: {module_data["title"]}')

            # Create assessment
            assessment_questions = [
                {
                    'question': 'What is Python?',
                    'options': [
                        'A programming language',
                        'A type of snake',
                        'A video game',
                        'An operating system'
                    ],
                    'correct_answer': 'A programming language'
                },
                {
                    'question': 'Which of the following is a valid variable name in Python?',
                    'options': [
                        'my_variable',
                        '2variable',
                        'my-variable',
                        'variable name'
                    ],
                    'correct_answer': 'my_variable'
                },
                {
                    'question': 'What does the print() function do?',
                    'options': [
                        'Displays output to the console',
                        'Prints a document',
                        'Creates a variable',
                        'Deletes a file'
                    ],
                    'correct_answer': 'Displays output to the console'
                },
                {
                    'question': 'Which keyword is used for conditional statements in Python?',
                    'options': [
                        'if',
                        'when',
                        'check',
                        'condition'
                    ],
                    'correct_answer': 'if'
                },
                {
                    'question': 'What is the correct way to create a string in Python?',
                    'options': [
                        '"Hello" or \'Hello\'',
                        'Hello',
                        '[Hello]',
                        '{Hello}'
                    ],
                    'correct_answer': '"Hello" or \'Hello\''
                }
            ]

            Assessment.objects.create(
                course=course,
                title='Python Fundamentals Assessment',
                passing_score=60,
                questions=assessment_questions
            )
            self.stdout.write(self.stdout.SUCCESS('Created assessment'))

        else:
            self.stdout.write(self.stdout.WARNING('Course already exists'))

        self.stdout.write(self.stdout.SUCCESS('Database seeded successfully!'))
