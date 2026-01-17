import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Course

print("Checking Course Prices conversion:")
for course in Course.objects.all():
    p = course.price
    print(f"Original: {p}, Type: {type(p)}")
    if hasattr(p, 'to_decimal'):
        print(f"Converted: {p.to_decimal()}, Type: {type(p.to_decimal())}")
    else:
        print("No to_decimal method")
