import os
import django
from django.contrib.auth import get_user_model
from django.urls import resolve

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

User = get_user_model()
admin = User.objects.get(username='admin')
admin.set_password('admin123')
admin.save()
print("ADMIN_PASSWORD_RESET: Success (admin123)")

# Check resolve behavior for admin login
try:
    res = resolve('/admin/login/')
    print(f"ADMIN_LOGIN_RESOLVE_NAME: {res.url_name}")
    print(f"ADMIN_LOGIN_RESOLVE_NAMESPACE: {res.namespace}")
except Exception as e:
    print(f"ADMIN_LOGIN_RESOLVE_ERROR: {str(e)}")

try:
    res = resolve('/login/')
    print(f"LOGIN_RESOLVE_NAME: {res.url_name}")
    print(f"LOGIN_RESOLVE_NAMESPACE: {res.namespace}")
except Exception as e:
    print(f"LOGIN_RESOLVE_ERROR: {str(e)}")
