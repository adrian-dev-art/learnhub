from django.db import models
from django.contrib.auth.models import AbstractUser
import secrets
import string


class User(AbstractUser):
    """Extended user model with email verification"""
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('owner', 'Owner'),
        ('penulis', 'Penulis'),
        ('pembaca', 'Pembaca'),
    ]

    email_verified = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, blank=True)
    profile_completed = models.BooleanField(default=False)
    # is_mentor is deprecated in favor of role='penulis'
    is_mentor = models.BooleanField(default=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='pembaca')
    bank_account_number = models.CharField(max_length=50, blank=True, help_text="For mentor payouts")

    class Meta:
        db_table = 'users'

    def save(self, *args, **kwargs):
        # Backward compatibility: sync is_mentor with role
        if self.is_mentor and self.role == 'pembaca':
            self.role = 'penulis'
        elif self.role == 'penulis':
            self.is_mentor = True

        # Sync admin role with Django permissions
        if self.role == 'admin':
            self.is_staff = True
            self.is_superuser = True

        super().save(*args, **kwargs)


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

    @property
    def display_price(self):
        """Return price as Python Decimal, handling MongoDB Decimal128"""
        if hasattr(self.price, 'to_decimal'):
            return self.price.to_decimal()
        return self.price


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
        total_modules = self.course.modules.count()
        if total_modules == 0:
            return 0
        completed_count = len(self.progress.get('completed_modules', [])) if self.progress else 0
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


class Commission(models.Model):
    """Commission records for Penulis and Admin"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('penulis', 'Penulis'),
        ('layanan', 'Layanan'),
    ]

    RATE_TYPE_CHOICES = [
        ('percentage', 'Percentage (%)'),
        ('flat', 'Flat (Rp)'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commissions')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='penulis')
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='commissions', null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    rate_type = models.CharField(max_length=20, choices=RATE_TYPE_CHOICES, default='percentage')
    rate_value = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Percentage or Flat amount")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'commissions'
        ordering = ['-created_at']

    @property
    def formatted_amount(self):
        """Format amount with thousand separator: 1.000.000"""
        return "{:,.0f}".format(self.amount).replace(",", ".")

    def __str__(self):
        return f"Commission - {self.user.username} - Rp {self.formatted_amount} ({self.status})"


class CommissionRate(models.Model):
    """Settings for commission percentages set by Owner"""
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('penulis', 'Penulis'),
        ('layanan', 'Layanan'),
    ]

    RATE_TYPE_CHOICES = [
        ('percentage', 'Percentage (%)'),
        ('flat', 'Flat (Rp)'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, help_text="Leave blank for global rate")
    rate_type = models.CharField(max_length=20, choices=RATE_TYPE_CHOICES, default='percentage')
    percentage = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="Used if type is percentage")
    flat_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, default=0, help_text="Used if type is flat")
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'commission_rates'
        unique_together = ['role', 'course']

    def __str__(self):
        course_str = self.course.title if self.course else "Global"
        rate_display = f"{self.percentage}%" if self.rate_type == 'percentage' else f"Rp {self.flat_amount}"
        return f"{self.get_role_display()} - {course_str}: {rate_display}"
