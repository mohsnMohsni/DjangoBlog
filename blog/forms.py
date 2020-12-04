from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Comment
from .validators import user_validator, password_validator


class RegisterForm(forms.Form):
    username = forms.CharField(label=_('Username'), max_length=150,
                               widget=forms.TextInput(attrs={'class': 'form-control my-2'}))
    email = forms.EmailField(label=_('Email'), required=True, help_text=_('valid email for reset password'),
                             widget=forms.EmailInput(attrs={'class': 'form-control my-2'}))
    password = forms.CharField(label=_('Password'), required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control my-2'}))
    password2 = forms.CharField(label=_('Confirm Password'), required=True,
                                widget=forms.PasswordInput(attrs={'class': 'form-control my-2'}))
    first_name = forms.CharField(label=_('First Name'), help_text=_('is not required'),
                                 widget=forms.TextInput(attrs={'class': 'form-control my-2'}))
    last_name = forms.CharField(label=_('Last Name'), help_text=_('is not required'),
                                widget=forms.TextInput(attrs={'class': 'form-control my-2'}))

    def clean(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password != password2:
            raise forms.ValidationError(
                'passwords are not match'
            )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user_validator(username)
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        password_validator(password)
        return password


class LoginForm(forms.Form):
    username = forms.CharField(label=_('Username'), max_length=150, required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control my- 2'}))
    password = forms.CharField(label=_('Password'), max_length=150, required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control my-2'}))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
