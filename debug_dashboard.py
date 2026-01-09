import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import User, Course, Enrollment

def test_dashboard_logic():
    try:
        user = User.objects.get(username='admin')
        print(f"Testing for user: {user.username}")

        courses = Course.objects.filter(mentor=user)
        print(f"Courses found: {courses.count()}")

        course_ids = [c.id for c in courses]
        print(f"Course IDs: {course_ids}")

        if not course_ids:
            print("No courses assigned to this mentor.")
            return

        enrollments = Enrollment.objects.filter(course_id__in=course_ids)
        print(f"Total enrollments: {enrollments.count()}")

        completed = enrollments.filter(completed=True).count()
        print(f"Completed enrollments: {completed}")

        print("Logic test passed!")
    except Exception as e:
        print(f"Logic test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_dashboard_logic()
