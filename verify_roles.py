import os
import django
import sys
import traceback

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser
from core.models import User
from core.views import admin_dashboard, owner_dashboard, mentor_dashboard, student_dashboard
from django.core.exceptions import PermissionDenied

def create_test_users():
    print("Creating test users...")
    users = {}
    roles = ['admin', 'owner', 'penulis', 'pembaca']

    for role in roles:
        try:
            username = f'test_{role}'
            email = f'{role}@example.com'
            print(f"Checking user: {username}")
            if not User.objects.filter(username=username).exists():
                print(f"Creating user: {username}")
                user = User.objects.create_user(username=username, email=email, password='password123', role=role)
                print(f"Created user: {username} with role: {role}")
            else:
                print(f"Updating user: {username}")
                user = User.objects.get(username=username)
                user.role = role
                user.save()
                print(f"Updated user: {username} to role: {role}")
            users[role] = user
        except Exception as e:
            print(f"Error creating/updating user {role}: {e}")
            traceback.print_exc()
    return users

def test_access(view_func, user, expected_success):
    factory = RequestFactory()
    request = factory.get('/')
    request.user = user

    view_name = view_func.__name__
    user_role = user.role if user.is_authenticated else 'Anonymous'

    try:
        response = view_func(request)
        if expected_success:
            if response.status_code == 302:
                print(f"[PASS] {user_role} accessed {view_name} (Redirected to {response.url})")
            elif response.status_code == 200:
                print(f"[PASS] {user_role} accessed {view_name}")
            else:
                print(f"[FAIL] {user_role} accessed {view_name} with status {response.status_code}")
        else:
            print(f"[FAIL] {user_role} accessed {view_name} (Should have been denied)")
    except PermissionDenied:
        if expected_success:
            print(f"[FAIL] {user_role} denied access to {view_name} (Should have succeeded)")
        else:
            print(f"[PASS] {user_role} denied access to {view_name}")
    except Exception as e:
        print(f"[ERROR] Testing {view_name} with {user_role}: {str(e)}")
        traceback.print_exc()

def run_verification():
    try:
        users = create_test_users()

        print("\n--- Testing Admin Dashboard ---")
        if 'admin' in users: test_access(admin_dashboard, users['admin'], True)
        if 'owner' in users: test_access(admin_dashboard, users['owner'], False)
        if 'penulis' in users: test_access(admin_dashboard, users['penulis'], False)
        if 'pembaca' in users: test_access(admin_dashboard, users['pembaca'], False)

        print("\n--- Testing Owner Dashboard ---")
        if 'admin' in users: test_access(owner_dashboard, users['admin'], False)
        if 'owner' in users: test_access(owner_dashboard, users['owner'], True)
        if 'penulis' in users: test_access(owner_dashboard, users['penulis'], False)
        if 'pembaca' in users: test_access(owner_dashboard, users['pembaca'], False)

        print("\n--- Testing Mentor Dashboard ---")
        if 'admin' in users: test_access(mentor_dashboard, users['admin'], False)
        if 'owner' in users: test_access(mentor_dashboard, users['owner'], False)
        if 'penulis' in users: test_access(mentor_dashboard, users['penulis'], True)
        if 'pembaca' in users: test_access(mentor_dashboard, users['pembaca'], False)

    except Exception as e:
        print(f"Fatal error in verification: {e}")
        traceback.print_exc()

if __name__ == '__main__':
    run_verification()
