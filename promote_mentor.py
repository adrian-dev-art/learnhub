import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import User, Course

def promote_to_mentor(username):
    try:
        user = User.objects.get(username=username)
        user.is_mentor = True
        user.save()
        print(f"User {username} promoted to mentor.")

        # Assign all courses to this mentor for demo purposes
        courses = Course.objects.all()
        for course in courses:
            # Fix for djongo Decimal128 issue
            if hasattr(course, 'price') and not isinstance(course.price, (int, float, str)):
                course.price = str(course.price)
            course.mentor = user
            course.save()
        print(f"Assigned {courses.count()} courses to {username}.")

    except User.DoesNotExist:
        print(f"User {username} not found.")

if __name__ == "__main__":
    # Promote the first user found
    user = User.objects.first()
    if user:
        promote_to_mentor(user.username)
    else:
        print("No users found.")
