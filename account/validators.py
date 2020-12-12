from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


def password_validator(password1, password2):
    if len(password1) < 8:
        raise forms.ValidationError(
            'password is similar'
        )
    if password1 != password2:
        raise forms.ValidationError(
            'passwords are not match'
        )
