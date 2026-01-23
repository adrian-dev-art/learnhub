import os
import django
import sys
import json
from decimal import Decimal

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.template import Context, Template
from core.templatetags.admin_dashboard_tags import get_admin_stats

def verify_dashboard():
    print("Verifying Admin Dashboard Analytics...")

    try:
        # 1. Test the template tag function directly
        stats = get_admin_stats()
        print("[PASS] get_admin_stats() returned data")

        # Verify keys
        required_keys = [
            'total_revenue', 'total_users', 'total_courses',
            'user_counts_json', 'top_courses_labels', 'top_courses_data',
            'recent_enrollments'
        ]

        for key in required_keys:
            if key in stats:
                print(f"[PASS] Key '{key}' present")
            else:
                print(f"[FAIL] Key '{key}' missing")

        # Verify JSON data
        try:
            json.loads(stats['user_counts_json'])
            print("[PASS] user_counts_json is valid JSON")
        except json.JSONDecodeError:
            print("[FAIL] user_counts_json is invalid JSON")

        # 2. Test Template Rendering
        print("\nTesting Template Rendering...")
        t = Template('{% load admin_dashboard_tags %}{% get_admin_stats as stats %}{{ stats.total_users }}')
        c = Context({})
        rendered = t.render(c)
        if rendered.strip().isdigit():
             print(f"[PASS] Template tag rendered successfully. Total users: {rendered.strip()}")
        else:
             print(f"[FAIL] Template tag rendering failed. Output: {rendered}")

    except Exception as e:
        print(f"[ERROR] Verification failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    verify_dashboard()
