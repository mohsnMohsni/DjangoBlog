from django.contrib.auth.models import User
from django import forms


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


def password_validator(password):
    if len(password) < 8:
        raise forms.ValidationError(
            'password is similar'
        )
