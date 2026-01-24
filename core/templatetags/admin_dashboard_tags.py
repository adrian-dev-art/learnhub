from django import template
from django.db.models import Sum, Count
from django.contrib.auth import get_user_model
from core.models import Course, Enrollment, User
from decimal import Decimal
import json

register = template.Library()

@register.simple_tag
def get_admin_stats():
    # 1. Total Revenue
    total_revenue = Decimal('0')
    completed_enrollments = Enrollment.objects.filter(payment_status='completed').select_related('course')

    for en in completed_enrollments:
        price = en.course.price
        if hasattr(price, 'to_decimal'):
            price = price.to_decimal()
        elif not isinstance(price, Decimal):
            price = Decimal(str(price))
        total_revenue += price

    # 2. User Distribution
    user_counts = {
        'admin': User.objects.filter(role='admin').count(),
        'owner': User.objects.filter(role='owner').count(),
        'penulis': User.objects.filter(role='penulis').count(),
        'pembaca': User.objects.filter(role='pembaca').count(),
    }

    # 3. Course Performance
    courses = Course.objects.all()
    course_data = []
    for c in courses:
        enrollment_count = Enrollment.objects.filter(course=c, payment_status='completed').count()
        course_data.append({
            'title': c.title,
            'count': enrollment_count
        })

    # Sort by count desc and take top 5
    top_courses = sorted(course_data, key=lambda x: x['count'], reverse=True)[:5]

    # 4. Recent Activity (Last 5 enrollments)
    recent_enrollments = Enrollment.objects.filter(payment_status='completed').select_related('user', 'course').order_by('-enrolled_at')[:5]

    return {
        'total_revenue': total_revenue,
        'total_users': User.objects.count(),
        'total_courses': Course.objects.count(),
        'user_counts_json': json.dumps(user_counts),
        'top_courses_labels': json.dumps([c['title'] for c in top_courses]),
        'top_courses_data': json.dumps([c['count'] for c in top_courses]),
        'recent_enrollments': recent_enrollments
    }

@register.filter
def rupiah(value):
    """Format value as Rupiah: 1.000.000"""
    try:
        if value is None:
            return "0"
        # Handle Decimal128 or other types
        if hasattr(value, 'to_decimal'):
            value = value.to_decimal()
        val = float(value)
        return "{:,.0f}".format(val).replace(",", ".")
    except (ValueError, TypeError):
        return value
