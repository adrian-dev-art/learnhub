import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

User = get_user_model()
admin = User.objects.filter(username='admin').first()

if admin:
    print(f"ADMIN_EXISTS: True")
    print(f"IS_STAFF: {admin.is_staff}")
    print(f"IS_SUPERUSER: {admin.is_superuser}")
    print(f"ROLE: {admin.role}")
    print(f"IS_ACTIVE: {admin.is_active}")
    print(f"HAS_PASSWORD: {admin.has_usable_password()}")
else:
    print("ADMIN_EXISTS: False")
