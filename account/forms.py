from django import forms
from django.contrib.auth import get_user_model
from .validators import password_validator, fullname_validator
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class RegisterForm(forms.ModelForm):
    password2 = forms.CharField(label=_('confirm password'), max_length=100, required=True,
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control text-info'}
                                ))

    class Meta:
        model = User
        fields = ('email', 'full_name', 'password')
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control text-info'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        password_validator(password1, password2)
        return password2

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        fullname_validator(full_name)
        return full_name


class LoginForm(forms.Form):
    email = forms.CharField(label=_('Email'), max_length=150, required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control my- 2'}))
    password = forms.CharField(label=_('Password'), max_length=150, required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control my-2'}))
