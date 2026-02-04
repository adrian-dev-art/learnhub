from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Course, Module, Assessment


class ModuleForm(forms.ModelForm):
    """Form for creating and editing course modules"""
    class Meta:
        model = Module
        fields = ('title', 'content_type', 'order', 'content', 'video_url', 'image', 'language', 'starter_code', 'expected_output', 'quiz_data')
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g., Understanding Variables'}),
            'content': forms.Textarea(attrs={'rows': 10, 'placeholder': 'Main lesson content (Markdown supported)...'}),
            'starter_code': forms.Textarea(attrs={'rows': 5, 'placeholder': '# Write starter code here...'}),
            'expected_output': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Expected output for validation...'}),
            'video_url': forms.URLInput(attrs={'placeholder': 'https://www.youtube.com/embed/...'}),
        }


class CourseForm(forms.ModelForm):
    """Form for creating and editing courses"""
    class Meta:
        model = Course
        fields = ('title', 'description', 'price', 'thumbnail', 'level', 'duration_hours', 'is_active')
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g., Advanced Python Mastery'}),
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Describe what students will learn...'}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
            'duration_hours': forms.NumberInput(attrs={'min': 1}),
        }


class CustomUserCreationForm(UserCreationForm):
    """Custom user registration form"""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-input'})


class ProfileForm(forms.ModelForm):
    """User profile completion form"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'bank_account_number')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'bank_account_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Bank Name - Account Number'}),
        }


class AssessmentSubmissionForm(forms.Form):
    """Dynamic form for assessment submission - supports both Question models and JSON data"""
    def __init__(self, *args, questions=None, **kwargs):
        super().__init__(*args, **kwargs)
        if questions:
            for i, question in enumerate(questions):
                # Handle both Model objects and dictionaries from JSON
                if hasattr(question, 'choices'):
                    # It's a Question model instance (from seeder)
                    choices = [(choice.id, choice.text) for choice in question.choices.all()]
                    q_id = question.id
                    q_label = question.text
                else:
                    # It's a dictionary (from questions_json / mentor side)
                    # We use enumerate index as ID if not provided
                    raw_options = question.get('options', [])
                    choices = []
                    for idx, opt in enumerate(raw_options):
                        # Handle both strings and objects
                        opt_text = opt.get('text', '') if isinstance(opt, dict) else opt
                        choices.append((idx, opt_text))
                    
                    q_id = i
                    q_label = question.get('question', '')

                self.fields[f'question_{q_id}'] = forms.ChoiceField(
                    label=q_label,
                    choices=choices,
                    widget=forms.RadioSelect(attrs={'class': 'form-radio'})
                )


class AssessmentForm(forms.ModelForm):
    """Form for creating and editing course assessments"""
    class Meta:
        model = Assessment
        fields = ('title', 'passing_score')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., Final Course Exam'}),
            'passing_score': forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'max': 100}),
        }
