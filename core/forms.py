from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Course, Module


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
        fields = ('first_name', 'last_name', 'email', 'phone')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
        }


class AssessmentSubmissionForm(forms.Form):
    """Dynamic form for assessment submission"""
    def __init__(self, *args, questions=None, **kwargs):
        super().__init__(*args, **kwargs)
        if questions:
            for i, question in enumerate(questions):
                choices = [(opt, opt) for opt in question.get('options', [])]
                self.fields[f'question_{i}'] = forms.ChoiceField(
                    label=question.get('question', ''),
                    choices=choices,
                    widget=forms.RadioSelect(attrs={'class': 'form-radio'})
                )
