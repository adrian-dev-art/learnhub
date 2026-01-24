from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin
from unfold.components import BaseComponent, register_component
from .models import Course, Module, Enrollment, Assessment, AssessmentResult, Certificate, User, Commission, CommissionRate
import json


@register_component
class UserDistributionChart(BaseComponent):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_counts = {
            'Admin': User.objects.filter(role='admin').count(),
            'Owner': User.objects.filter(role='owner').count(),
            'Mentor': User.objects.filter(role='penulis').count(),
            'Student': User.objects.filter(role='pembaca').count(),
        }

        context.update({
            "height": 300,
            "data": json.dumps({
                "labels": list(user_counts.keys()),
                "datasets": [{
                    "label": "Users",
                    "data": list(user_counts.values()),
                    "backgroundColor": [
                        "var(--color-primary-700)",
                        "var(--color-primary-500)",
                        "var(--color-primary-300)",
                        "var(--color-primary-100)",
                    ],
                }]
            })
        })
        return context


@register_component
class CoursePerformanceChart(BaseComponent):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        courses = Course.objects.all()
        course_data = []
        for c in courses:
            enrollment_count = Enrollment.objects.filter(course=c, payment_status='completed').count()
            course_data.append({
                'title': c.title,
                'count': enrollment_count
            })

        top_courses = sorted(course_data, key=lambda x: x['count'], reverse=True)[:5]

        context.update({
            "height": 300,
            "data": json.dumps({
                "labels": [c['title'] for c in top_courses],
                "datasets": [{
                    "label": "Enrollments",
                    "data": [c['count'] for c in top_courses],
                    "backgroundColor": "var(--color-primary-600)",
                }]
            })
        })
        return context


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin, ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role', 'is_mentor', 'phone', 'profile_completed')}),
    )


@admin.register(Course)
class CourseAdmin(ModelAdmin):
    list_display = ('title', 'price', 'level', 'duration_hours', 'is_active', 'created_at')
    list_filter = ('level', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)


@admin.register(Module)
class ModuleAdmin(ModelAdmin):
    list_display = ('title', 'course', 'content_type', 'order')
    list_filter = ('content_type', 'course')
    search_fields = ('title', 'content')
    ordering = ('course', 'order')


@admin.register(Enrollment)
class EnrollmentAdmin(ModelAdmin):
    list_display = ('user', 'course', 'access_key', 'payment_status', 'completed', 'enrolled_at')
    list_filter = ('payment_status', 'completed', 'enrolled_at')
    search_fields = ('user__username', 'course__title', 'access_key')
    readonly_fields = ('access_key', 'enrolled_at')


@admin.register(Assessment)
class AssessmentAdmin(ModelAdmin):
    list_display = ('title', 'course', 'passing_score')
    search_fields = ('title', 'course__title')


@admin.register(AssessmentResult)
class AssessmentResultAdmin(ModelAdmin):
    list_display = ('user', 'assessment', 'score', 'passed', 'completed_at')
    list_filter = ('passed', 'completed_at')
    search_fields = ('user__username', 'assessment__title')
    readonly_fields = ('completed_at',)


@admin.register(Certificate)
class CertificateAdmin(ModelAdmin):
    list_display = ('user', 'course', 'certificate_id', 'issued_at')
    search_fields = ('user__username', 'course__title', 'certificate_id')
    readonly_fields = ('certificate_id', 'issued_at')


@admin.register(Commission)
class CommissionAdmin(ModelAdmin):
    list_display = ('user', 'formatted_amount_display', 'rate_type', 'rate_value', 'status', 'course', 'created_at')
    list_filter = ('status', 'rate_type', 'user__role', 'created_at')
    search_fields = ('user__username', 'course__title', 'note')
    readonly_fields = ('created_at',)
    actions = ['mark_as_paid']

    def formatted_amount_display(self, obj):
        return f"Rp {obj.formatted_amount}"
    formatted_amount_display.short_description = 'Amount'
    search_fields = ('user__username', 'course__title', 'note')
    readonly_fields = ('created_at',)
    actions = ['mark_as_paid']

    @admin.action(description="Mark selected commissions as paid")
    def mark_as_paid(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='paid', paid_at=timezone.now())


@admin.register(CommissionRate)
class CommissionRateAdmin(ModelAdmin):
    list_display = ('role', 'course', 'rate_type', 'percentage', 'flat_amount', 'is_active')
    list_filter = ('role', 'rate_type', 'is_active')
    search_fields = ('course__title',)


# Admin Site Customization
admin.site.site_header = "GampangBelajar"
admin.site.site_title = "GampangBelajar Admin Portal"
admin.site.index_title = "Welcome to GampangBelajar Management System"
