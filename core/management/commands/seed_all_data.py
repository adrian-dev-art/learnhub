"""
Comprehensive data seeder for GampangBelajar Course Platform
Creates users, courses, modules, and assessments
Usage: python manage.py seed_all_data
"""

from django.core.management.base import BaseCommand
from core.models import User, Course, Module, Assessment
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):
    help = 'Seeds database with comprehensive sample data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting comprehensive data seeding...'))

        # Create users
        self.create_users()

        # Create courses
        self.create_python_course()
        self.create_javascript_course()
        self.create_web_dev_course()
        self.create_data_science_course()

        self.stdout.write(self.style.SUCCESS('\n✅ Database seeded successfully!'))
        self.stdout.write(self.style.SUCCESS('\nTest Accounts Created:'))
        self.stdout.write('  - Username: admin, Password: admin123 (Admin)')
        self.stdout.write('  - Username: owner, Password: owner123 (Owner)')
        self.stdout.write('  - Username: mentor, Password: mentor123 (Mentor/Penulis)')
        self.stdout.write('  - Username: student1, Password: student123 (Student/Pembaca)')
        self.stdout.write('  - Username: student2, Password: student123 (Student/Pembaca)')

    def create_users(self):
        """Create sample users"""
        self.stdout.write('\nCreating users...')

        # Admin user
        if not User.objects.filter(username='admin').exists():
            User.objects.create(
                username='admin',
                email='admin@gampangbelajar.com',
                password=make_password('admin123'),
                first_name='Admin',
                last_name='User',
                role='admin',
                is_staff=True,
                is_superuser=True,
                profile_completed=True
            )
            self.stdout.write('  ✓ Created admin user')

        # Owner user
        if not User.objects.filter(username='owner').exists():
            User.objects.create(
                username='owner',
                email='owner@gampangbelajar.com',
                password=make_password('owner123'),
                first_name='Owner',
                last_name='User',
                role='owner',
                profile_completed=True
            )
            self.stdout.write('  ✓ Created owner user')

        # Mentor user
        if not User.objects.filter(username='mentor').exists():
            User.objects.create(
                username='mentor',
                email='mentor@gampangbelajar.com',
                password=make_password('mentor123'),
                first_name='Mentor',
                last_name='User',
                role='penulis',
                is_mentor=True,
                profile_completed=True
            )
            self.stdout.write('  ✓ Created mentor user')

        # Student users
        for i in range(1, 3):
            if not User.objects.filter(username=f'student{i}').exists():
                User.objects.create(
                    username=f'student{i}',
                    email=f'student{i}@example.com',
                    password=make_password('student123'),
                    first_name=f'Student',
                    last_name=f'{i}',
                    role='pembaca',
                    profile_completed=True
                )
                self.stdout.write(f'  ✓ Created student{i}')

    def create_python_course(self):
        """Create Python Programming course"""
        self.stdout.write('\nCreating Python Programming course...')

        course, created = Course.objects.get_or_create(
            title='Python Programming Fundamentals',
            defaults={
                'description': 'Master Python from scratch! Learn variables, data types, control structures, functions, and OOP. Perfect for beginners with hands-on coding exercises.',
                'price': 49.99,
                'level': 'beginner',
                'duration_hours': 12,
                'is_active': True
            }
        )

        if created:
            self.stdout.write('  ✓ Course created')

            # Modules
            modules_data = [
                {
                    'title': 'Introduction to Python',
                    'order': 1,
                    'content_type': 'text',
                    'content': '''Welcome to Python Programming!

Python is a powerful, easy-to-learn programming language used for web development, data science, automation, and more.

**What you'll learn:**
- Variables and data types
- Control structures (if, loops)
- Functions and modules
- Object-oriented programming
- File handling and error handling

**Course Requirements:**
- No prior programming experience needed
- Computer with Python installed
- Willingness to practice coding

Let's start your programming journey!'''
                },
                {
                    'title': 'Your First Python Program',
                    'order': 2,
                    'content_type': 'code',
                    'content': 'Let\'s write your first Python program! The traditional "Hello, World!" is a great starting point.',
                    'starter_code': '# Write your code here\nprint("Hello, World!")',
                    'expected_output': 'Hello, World!\n'
                },
                {
                    'title': 'Variables and Data Types',
                    'order': 3,
                    'content_type': 'text',
                    'content': '''## Variables in Python

Variables store data values. In Python, you don't need to declare variable types.

**Creating Variables:**
```python
name = "John"
age = 25
height = 5.9
is_student = True
```

**Data Types:**
- **str**: Text (strings)
- **int**: Whole numbers
- **float**: Decimal numbers
- **bool**: True/False values
- **list**: Ordered collection [1, 2, 3]
- **dict**: Key-value pairs {"name": "John"}

**Type Checking:**
```python
type(name)  # <class 'str'>
type(age)   # <class 'int'>
```'''
                },
                {
                    'title': 'Practice: Working with Variables',
                    'order': 4,
                    'content_type': 'code',
                    'content': 'Create variables for your personal information and print them using f-strings.',
                    'starter_code': '''# Create variables
name = "Your Name"
age = 25
city = "Your City"
favorite_language = "Python"

# Print using f-strings
print(f"Hello! My name is {name}")
print(f"I am {age} years old")
print(f"I live in {city}")
print(f"My favorite programming language is {favorite_language}")'''
                },
                {
                    'title': 'Python Basics Video Tutorial',
                    'order': 5,
                    'content_type': 'video',
                    'content': 'Watch this comprehensive video tutorial covering Python basics and syntax.',
                    'video_url': 'https://www.youtube.com/embed/rfscVS0vtbw'
                },
                {
                    'title': 'Control Flow: If Statements',
                    'order': 6,
                    'content_type': 'code',
                    'content': 'Learn conditional logic with if-elif-else statements. Write a program to check if a number is positive, negative, or zero.',
                    'starter_code': '''# Check if a number is positive, negative, or zero
number = 10

if number > 0:
    print("Positive")
elif number < 0:
    print("Negative")
else:
    print("Zero")

# Try changing the number value!'''
                },
                {
                    'title': 'Loops: For and While',
                    'order': 7,
                    'content_type': 'code',
                    'content': 'Practice loops to repeat actions. Print numbers from 1 to 10.',
                    'starter_code': '''# For loop example
print("Counting with for loop:")
for i in range(1, 11):
    print(i)

# While loop example
print("\\nCounting with while loop:")
count = 1
while count <= 10:
    print(count)
    count += 1'''
                },
                {
                    'title': 'Course Summary',
                    'order': 8,
                    'content_type': 'text',
                    'content': '''## Congratulations!

You've completed the Python Programming Fundamentals course!

**You've learned:**
✓ Python syntax and basic concepts
✓ Variables and data types
✓ Control flow (if statements)
✓ Loops (for and while)
✓ Writing and running Python code

**Next Steps:**
1. Take the assessment to test your knowledge
2. Earn your certificate of completion
3. Explore advanced Python courses
4. Build your own projects!

Remember: Practice makes perfect. Keep coding!'''
                }
            ]

            for module_data in modules_data:
                module_data['course'] = course
                Module.objects.create(**module_data)

            self.stdout.write(f'  ✓ Created {len(modules_data)} modules')

            # Assessment
            assessment_questions = [
                {
                    'question': 'What is Python primarily used for?',
                    'options': [
                        'Web development, data science, and automation',
                        'Only web development',
                        'Only mobile apps',
                        'Hardware programming only'
                    ],
                    'correct_answer': 'Web development, data science, and automation'
                },
                {
                    'question': 'Which of these is a valid variable name?',
                    'options': ['my_variable', '2variable', 'my-variable', 'variable name'],
                    'correct_answer': 'my_variable'
                },
                {
                    'question': 'What does print() do in Python?',
                    'options': [
                        'Displays output to the console',
                        'Prints a document',
                        'Creates a variable',
                        'Saves a file'
                    ],
                    'correct_answer': 'Displays output to the console'
                },
                {
                    'question': 'Which data type represents True or False?',
                    'options': ['bool', 'int', 'str', 'float'],
                    'correct_answer': 'bool'
                },
                {
                    'question': 'What keyword is used for conditional statements?',
                    'options': ['if', 'when', 'check', 'condition'],
                    'correct_answer': 'if'
                }
            ]

            Assessment.objects.get_or_create(
                course=course,
                defaults={
                    'title': 'Python Fundamentals Assessment',
                    'passing_score': 60,
                    'questions': assessment_questions
                }
            )
            self.stdout.write('  ✓ Created assessment')

    def create_javascript_course(self):
        """Create JavaScript course"""
        self.stdout.write('\nCreating JavaScript course...')

        course, created = Course.objects.get_or_create(
            title='JavaScript Essentials',
            defaults={
                'description': 'Learn JavaScript, the language of the web! Master DOM manipulation, events, ES6 features, and async programming. Build interactive web applications.',
                'price': 59.99,
                'level': 'beginner',
                'duration_hours': 15,
                'is_active': True
            }
        )

        if created:
            modules_data = [
                {
                    'title': 'Introduction to JavaScript',
                    'order': 1,
                    'content_type': 'text',
                    'content': '''# Welcome to JavaScript!

JavaScript is the programming language of the web, enabling interactive and dynamic websites.

**What you'll learn:**
- JavaScript syntax and basics
- DOM manipulation
- Event handling
- ES6+ features
- Asynchronous programming

**Applications:**
- Interactive websites
- Web applications
- Server-side (Node.js)
- Mobile apps (React Native)

Let's dive in!'''
                },
                {
                    'title': 'JavaScript Basics',
                    'order': 2,
                    'content_type': 'code',
                    'content': 'Learn JavaScript variables and console logging.',
                    'starter_code': '''// Variables in JavaScript
let name = "JavaScript";
const year = 1995;
var isAwesome = true;

// Output
console.log("Hello, " + name + "!");
console.log(`Created in ${year}`);
console.log("Awesome?", isAwesome);'''
                },
                {
                    'title': 'Functions and Arrow Functions',
                    'order': 3,
                    'content_type': 'code',
                    'content': 'Understand functions and modern arrow syntax.',
                    'starter_code': '''// Traditional function
function greet(name) {
    return "Hello, " + name;
}

// Arrow function
const greetArrow = (name) => {
    return `Hello, ${name}`;
};

// Short arrow function
const greetShort = name => `Hello, ${name}`;

console.log(greet("World"));
console.log(greetArrow("ES6"));
console.log(greetShort("Arrow"));'''
                }
            ]

            for module_data in modules_data:
                module_data['course'] = course
                Module.objects.create(**module_data)

            self.stdout.write(f'  ✓ Created {len(modules_data)} modules')

            # Assessment
            questions = [
                {
                    'question': 'Which keyword is used for constants in JavaScript?',
                    'options': ['const', 'let', 'var', 'constant'],
                    'correct_answer': 'const'
                },
                {
                    'question': 'What does DOM stand for?',
                    'options': [
                        'Document Object Model',
                        'Data Object Model',
                        'Digital Object Method',
                        'Document Order Management'
                    ],
                    'correct_answer': 'Document Object Model'
                },
                {
                    'question': 'Which symbol is used for arrow functions?',
                    'options': ['=>', '->', '~>', '>>'],
                    'correct_answer': '=>'
                }
            ]

            Assessment.objects.get_or_create(
                course=course,
                defaults={
                    'title': 'JavaScript Essentials Quiz',
                    'passing_score': 70,
                    'questions': questions
                }
            )
            self.stdout.write('  ✓ Created assessment')

    def create_web_dev_course(self):
        """Create Web Development course"""
        self.stdout.write('\nCreating Web Development course...')

        course, created = Course.objects.get_or_create(
            title='Complete Web Development Bootcamp',
            defaults={
                'description': 'Become a full-stack web developer! Learn HTML, CSS, JavaScript, responsive design, and modern frameworks. Build real-world projects from scratch.',
                'price': 79.99,
                'level': 'intermediate',
                'duration_hours': 25,
                'is_active': True
            }
        )

        if created:
            modules_data = [
                {
                    'title': 'Web Development Overview',
                    'order': 1,
                    'content_type': 'text',
                    'content': '''# Web Development Bootcamp

Learn to build modern, responsive websites and web applications!

**Technologies Covered:**
- HTML5 (Structure)
- CSS3 (Styling)
- JavaScript (Interactivity)
- Responsive Design
- Modern Frameworks

**Career Path:**
- Frontend Developer
- Full-Stack Developer
- Web Designer
- UI/UX Developer

Build your portfolio while learning!'''
                },
                {
                    'title': 'HTML Structure',
                    'order': 2,
                    'content_type': 'text',
                    'content': '''## HTML Basics

HTML (HyperText Markup Language) provides structure to web pages.

**Basic Structure:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>My Page</title>
</head>
<body>
    <h1>Welcome</h1>
    <p>This is a paragraph.</p>
</body>
</html>
```

**Common Tags:**
- Headings: h1, h2, h3
- Paragraph: p
- Links: a
- Images: img
- Lists: ul, ol, li'''
                },
                {
                    'title': 'CSS Styling Fundamentals',
                    'order': 3,
                    'content_type': 'text',
                    'content': '''## CSS Basics

CSS (Cascading Style Sheets) adds design and layout to HTML.

**Syntax:**
```css
selector {
    property: value;
}
```

**Examples:**
```css
h1 {
    color: blue;
    font-size: 32px;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
}
```

**Key Concepts:**
- Selectors (class, id, element)
- Flexbox & Grid layouts
- Responsive design
- Animations'''
                }
            ]

            for module_data in modules_data:
                module_data['course'] = course
                Module.objects.create(**module_data)

            self.stdout.write(f'  ✓ Created {len(modules_data)} modules')

            # Assessment
            questions = [
                {
                    'question': 'What does HTML stand for?',
                    'options': [
                        'HyperText Markup Language',
                        'High Tech Modern Language',
                        'Home Tool Markup Language',
                        'Hyperlinks and Text Markup Language'
                    ],
                    'correct_answer': 'HyperText Markup Language'
                },
                {
                    'question': 'Which property changes text color in CSS?',
                    'options': ['color', 'text-color', 'font-color', 'text-style'],
                    'correct_answer': 'color'
                }
            ]

            Assessment.objects.get_or_create(
                course=course,
                defaults={
                    'title': 'Web Development Quiz',
                    'passing_score': 65,
                    'questions': questions
                }
            )
            self.stdout.write('  ✓ Created assessment')

    def create_data_science_course(self):
        """Create Data Science course"""
        self.stdout.write('\nCreating Data Science course...')

        course, created = Course.objects.get_or_create(
            title='Data Science with Python',
            defaults={
                'description': 'Master data science fundamentals! Learn NumPy, Pandas, data visualization, machine learning basics, and statistical analysis. Work with real datasets.',
                'price': 89.99,
                'level': 'advanced',
                'duration_hours': 30,
                'is_active': True
            }
        )

        if created:
            modules_data = [
                {
                    'title': 'Introduction to Data Science',
                    'order': 1,
                    'content_type': 'text',
                    'content': '''# Data Science with Python

Learn to extract insights from data using Python!

**What is Data Science?**
Data science combines statistics, programming, and domain expertise to extract meaningful insights from data.

**Tools You'll Learn:**
- NumPy (numerical computing)
- Pandas (data manipulation)
- Matplotlib/Seaborn (visualization)
- Scikit-learn (machine learning)

**Applications:**
- Business analytics
- Predictive modeling
- Data visualization
- Machine learning

Let's unlock the power of data!'''
                },
                {
                    'title': 'NumPy Basics',
                    'order': 2,
                    'content_type': 'code',
                    'content': 'Learn NumPy for numerical computing and array operations.',
                    'starter_code': '''# Note: This is a simulation since NumPy isn't installed
# In real environment, you would:
# import numpy as np

# Create arrays
arr = [1, 2, 3, 4, 5]
print("Array:", arr)

# Mathematical operations
doubled = [x * 2 for x in arr]
print("Doubled:", doubled)

# Sum
total = sum(arr)
print("Sum:", total)

# Mean
mean = total / len(arr)
print("Mean:", mean)'''
                },
                {
                    'title': 'Data Analysis Project',
                    'order': 3,
                    'content_type': 'text',
                    'content': '''## Final Project: Analyze Real Data

Apply your skills to a real-world dataset!

**Project Steps:**
1. Load and explore data
2. Clean and preprocess
3. Perform statistical analysis
4. Create visualizations
5. Draw conclusions

**Deliverables:**
- Jupyter notebook
- Data visualizations
- Analysis report

**Tips:**
- Start with exploratory analysis
- Document your findings
- Use clear visualizations
- Validate your assumptions

Good luck with your analysis!'''
                }
            ]

            for module_data in modules_data:
                module_data['course'] = course
                Module.objects.create(**module_data)

            self.stdout.write(f'  ✓ Created {len(modules_data)} modules')

            # Assessment
            questions = [
                {
                    'question': 'Which library is used for data manipulation in Python?',
                    'options': ['Pandas', 'NumPy', 'Matplotlib', 'Seaborn'],
                    'correct_answer': 'Pandas'
                },
                {
                    'question': 'What does EDA stand for in data science?',
                    'options': [
                        'Exploratory Data Analysis',
                        'External Data Access',
                        'Enhanced Data Algorithm',
                        'Experimental Data Application'
                    ],
                    'correct_answer': 'Exploratory Data Analysis'
                },
                {
                    'question': 'NumPy is primarily used for?',
                    'options': [
                        'Numerical computing',
                        'Web scraping',
                        'Database management',
                        'Image editing'
                    ],
                    'correct_answer': 'Numerical computing'
                }
            ]

            Assessment.objects.get_or_create(
                course=course,
                defaults={
                    'title': 'Data Science Fundamentals Quiz',
                    'passing_score': 70,
                    'questions': questions
                }
            )
            self.stdout.write('  ✓ Created assessment')
