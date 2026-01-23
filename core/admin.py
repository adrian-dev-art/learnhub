from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin
from .models import Course, Module, Enrollment, Assessment, AssessmentResult, Certificate, User


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


# Admin Site Customization
admin.site.site_header = "Learning App Administration"
admin.site.site_title = "Learning App Admin Portal"
admin.site.index_title = "Welcome to the Learning App Management System"
