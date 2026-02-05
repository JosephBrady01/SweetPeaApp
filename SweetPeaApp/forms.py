from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Testimonials
from .models import ResourceDocument



# --------------------------
# User Registration Form
# --------------------------
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


# --------------------------
# Testimonial Form (Portal)
# --------------------------
class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonials
        fields = ["body", "reviewer", "location"]   # 👈 what admins can edit in portal

        widgets = {
            "body": forms.Textarea(attrs={
                "rows": 5,
                "placeholder": "Write the testimonial here…",
                "class": "form-control"
            }),
            "reviewer": forms.TextInput(attrs={
                "placeholder": "Name (optional)",
                "class": "form-control"
            }),
            "location": forms.TextInput(attrs={
                "placeholder": "Location (optional)",
                "class": "form-control"
            }),
        }
# --------------------------
# Resource Form (Portal)
# --------------------------
class ResourceDocumentForm(forms.ModelForm):
    class Meta:
        model = ResourceDocument
        fields = ["title", "description", "file", "is_published"]