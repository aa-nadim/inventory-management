from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        # Check if email is already taken
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already registered.")
        
        # Email format validation
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            raise ValidationError("Enter a valid email address.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        # Check if username is already taken
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        
        # Ensure the username is alphanumeric
        if not username.isalnum():
            raise ValidationError("Username must be alphanumeric.")
        
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
