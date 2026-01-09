from django.db import models
from django.contrib.auth.models import AbstractUser
import secrets
import string


class User(AbstractUser):
    """Extended user model with email verification"""
    email_verified = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, blank=True)
    profile_completed = models.BooleanField(default=False)
    is_mentor = models.BooleanField(default=False)

    class Meta:
        db_table = 'users'


class Course(models.Model):
    """Course model"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    mentor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='mentored_courses')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    thumbnail = models.ImageField(upload_to='courses/thumbnails/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    duration_hours = models.IntegerField(default=10)
    level = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ], default='beginner')

    class Meta:
        db_table = 'courses'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Module(models.Model):
    """Course module/lesson"""
    CONTENT_TYPES = [
        ('text', 'Text'),
        ('video', 'Video'),
        ('code', 'Code Challenge'),
    ]

    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    order = models.IntegerField(default=0)
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPES)
    content = models.TextField()  # Text content or code
    video_url = models.URLField(blank=True)  # YouTube URL
    image = models.ImageField(upload_to='courses/images/', blank=True, null=True)

    # For code exercises
    language = models.CharField(max_length=20, choices=[
        ('python', 'Python'),
        ('javascript', 'JavaScript'),
        ('html', 'HTML'),
    ], default='python')
    starter_code = models.TextField(blank=True)
    expected_output = models.TextField(blank=True)

    # Optional Quiz Data
    quiz_data = models.JSONField(default=list, blank=True)  # List of {question, options, correct_answer}

    class Meta:
        db_table = 'modules'
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Enrollment(models.Model):
    """User course enrollment"""
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    access_key = models.CharField(max_length=32, unique=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    progress = models.JSONField(default=dict)  # Track completed modules
    completed = models.BooleanField(default=False)

    class Meta:
        db_table = 'enrollments'
        unique_together = ['user', 'course']

    def save(self, *args, **kwargs):
        if not self.access_key:
            self.access_key = self.generate_access_key()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_access_key():
        """Generate a secure random access key"""
        chars = string.ascii_uppercase + string.digits
        return ''.join(secrets.choice(chars) for _ in range(16))

    @property
    def progress_percentage(self):
        """Calculate progress percentage"""
        total_modules = Module.objects.filter(course_id=self.course_id).count()
        if total_modules == 0:
            return 0
        completed_count = len(self.progress.keys()) if self.progress else 0
        return int((completed_count / total_modules) * 100)

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"


class Assessment(models.Model):
    """Course assessment/quiz"""
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='assessment')
    title = models.CharField(max_length=200)
    passing_score = models.IntegerField(default=70)
    questions = models.JSONField()  # List of questions with options and correct answers

    class Meta:
        db_table = 'assessments'

    def __str__(self):
        return f"Assessment - {self.course.title}"


class AssessmentResult(models.Model):
    """User assessment results"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    score = models.IntegerField()
    answers = models.JSONField()  # User's answers
    passed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'assessment_results'

    def __str__(self):
        return f"{self.user.username} - {self.assessment.course.title} - {self.score}%"


class Certificate(models.Model):
    """Course completion certificate"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE)
    certificate_id = models.CharField(max_length=100, unique=True)
    issued_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'certificates'

    def save(self, *args, **kwargs):
        if not self.certificate_id:
            self.certificate_id = f"CERT-{secrets.token_hex(8).upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Certificate - {self.user.username} - {self.course.title}"
