# MongoDB Configuration Guide

Since you have MongoDB Compass installed locally, follow these steps to configure the app to use MongoDB:

## 1. Install djongo (MongoDB connector for Django)

```bash
pip install djongo==1.3.6 pymongo==3.12.3 sqlparse==0.2.4
```

## 2. Update settings.py

In `config/settings.py`, replace the DATABASES configuration (around line 60):

```python
# Database - MongoDB via djongo
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'courseplatform',  # Your database name
        'ENFORCE_SCHEMA': False,
        'CLIENT': {
            'host': 'localhost',
            'port': 27017,
        }
    }
}
```

## 3. Make sure MongoDB is running

Open MongoDB Compass and connect to `mongodb://localhost:27017`

## 4. Reset and migrate database

```bash
# Remove SQLite database
Remove-Item -Force db.sqlite3

# Remove old migrations
Remove-Item -Recurse -Force core\migrations

# Create new migrations
py manage.py makemigrations core
py manage.py migrate

# Seed data
py manage.py seed_all_data

# Run server
py manage.py runserver
```

## Current Status

✅ **Enrollment Flow Updated**: Users can now enroll WITHOUT logging in first!
- Non-logged-in users: Fill profile + create account + enroll in one step
- Logged-in users: Fill profile + enroll
- Both receive access key via email

✅ **Course Catalog**: Shows "Enroll Now" button for everyone
✅ **4 Sample Courses**: Python, JavaScript, Web Dev, Data Science
✅ **Test Accounts**: admin/admin123, student1/student123

## MongoDB in Compass

After seeding, you'll see these collections in MongoDB Compass:
- `users` - User accounts
- `courses` - Course data
- `modules` - Course content
- `enrollments` - User enrollments with access keys
- `assessments` - Quizzes
- `certificates` - Generated certificates

The app is currently running with **SQLite** (simpler for testing). Switch to MongoDB when you're ready!
