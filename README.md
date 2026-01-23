# GampangBelajar Course Platform

A modern, lightweight Django-based interactive course platform with MongoDB integration.

## Features

- Modern, minimalist UI with Google Material Icons
- Interactive Python code compiler (browser-based)
- Course catalog and enrollment system
- Payment integration (demo mode included)
- User profile management
- Email delivery for access keys
- YouTube video embedding
- Assessment system with auto-grading
- PDF certificate generation
- Admin interface for course management

## Tech Stack

- **Backend**: Django 4.2 (lightweight configuration)
- **Database**: MongoDB (via djongo)
- **Frontend**: HTML, CSS (modern design system), Vanilla JavaScript
- **Icons**: Google Material Icons
- **PDF Generation**: ReportLab

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file from `.env.example`:

```bash
copy .env.example .env
```

Edit `.env` and configure:
- MongoDB connection (local or Atlas)
- Email settings (Gmail SMTP recommended)
- Secret key

### 3. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Admin User

```bash
python manage.py createsuperuser
```

### 5. Seed Sample Data

```bash
python manage.py seed_data
```

This creates a sample "Python Programming Fundamentals" course with modules and assessment.

### 6. Run Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000` to access the platform.

## Usage Flow

1. **Browse Catalog**: Visit `/catalog/` to see available courses
2. **Register**: Create an account at `/register/`
3. **Enroll**: Select a course and complete payment (demo mode)
4. **Complete Profile**: Fill in your profile information
5. **Receive Access Key**: Check your email for the course access key
6. **Learn**: Access course modules with interactive code exercises
7. **Assess**: Complete the assessment at the end
8. **Certify**: Download your PDF certificate upon passing

## Admin Panel

Access the admin panel at `/admin/` to:
- Create and manage courses
- Add modules (text, code, video, image)
- Create assessments
- View enrollments and certificates

## Code Compiler

The platform includes a sandboxed Python code compiler that:
- Executes user code in a temporary file
- Has a 5-second timeout for safety
- Captures stdout and stderr
- Runs in an isolated environment

## Project Structure

```
learningapp/
├── config/          # Django settings and configuration
├── core/            # Main application
│   ├── models.py    # MongoDB models
│   ├── views.py     # Views and business logic
│   ├── forms.py     # Django forms
│   ├── utils.py     # Utility functions
│   ├── admin.py     # Admin configuration
│   └── management/  # Custom commands
├── templates/       # HTML templates
├── static/          # CSS and JavaScript
└── requirements.txt
```

## Security Notes

- The code compiler is sandboxed with timeout limits
- Payment is in demo mode by default
- Email credentials should be stored in environment variables
- Change SECRET_KEY in production

## License

This project is for educational purposes.
