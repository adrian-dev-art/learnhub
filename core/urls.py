from django.urls import path
from . import views

urlpatterns = [
    # Home and catalog
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),

    # Enrollment and payment
    path('payment/<int:course_id>/', views.payment, name='payment'),

    # Course viewer
    path('course-viewer/<int:enrollment_id>/', views.course_viewer, name='course_viewer'),
    path('module-complete/<int:enrollment_id>/<int:module_id>/', views.mark_module_complete, name='mark_module_complete'),
    path('module-quiz-save/<int:enrollment_id>/<int:module_id>/', views.save_module_quiz_progress, name='save_module_quiz_progress'),

    # Code execution
    path('execute-code/', views.execute_code, name='execute_code'),

    # Assessment
    path('assessment/<int:enrollment_id>/', views.assessment_view, name='assessment_view'),

    # Certificate
    path('certificate/<int:enrollment_id>/', views.certificate_view, name='certificate_view'),
    path('download-certificate/<int:certificate_id>/', views.download_certificate, name='download_certificate'),

    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # User Features
    path('schedule/', views.schedule, name='schedule'),
    path('progress/', views.progress_view, name='progress'),
    path('settings/', views.settings_view, name='settings'),

    # Mentor Admin
    path('mentor/', views.mentor_dashboard, name='mentor_dashboard'),
    path('mentor/course/add/', views.mentor_course_add, name='mentor_course_add'),
    path('mentor/course/<int:course_id>/edit/', views.mentor_course_edit, name='mentor_course_edit'),
    path('mentor/course/<int:course_id>/import/', views.mentor_course_import_doc, name='mentor_course_import_doc'),
    path('mentor/course/<int:course_id>/', views.mentor_course_detail, name='mentor_course_detail'),
    path('mentor/commission/', views.mentor_commission_detail, name='mentor_commission_detail'),
    path('mentor/course/<int:course_id>/assessment/', views.mentor_assessment_edit, name='mentor_assessment_edit'),
    path('mentor/assessment/template/', views.download_assessment_template, name='download_assessment_template'),
    path('mentor/assessment/import/', views.import_assessment_questions, name='import_assessment_questions'),
    path('mentor/course/<int:course_id>/module/add/', views.mentor_module_add, name='mentor_module_add'),
    path('mentor/module/<int:module_id>/edit/', views.mentor_module_edit, name='mentor_module_edit'),
    path('mentor/module/import-content/', views.import_module_content, name='import_module_content'),
]
