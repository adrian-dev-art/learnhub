import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Course

print("Checking Course Prices:")
for course in Course.objects.all():
    print(f"ID: {course.id}, Title: {course.title}, Price: {course.price}, Type: {type(course.price)}")
