from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


def user_validator(username):
    user = None
    try:
        user = User.objects.get(username=username)
    except:
        pass
    if username[0].isdigit() or user is not None:
        raise forms.ValidationError(
            'username not valid'
        )
    if username.__contains__(' ') or username.__contains__('-'):
        raise forms.ValidationError(
            'username not valid'
        )


def password_validator(password1, password2):
    if len(password1) < 8:
        raise forms.ValidationError(
            'password is similar'
        )
    if password1 != password2:
        raise forms.ValidationError(
            'passwords are not match'
        )
