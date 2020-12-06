from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Comment
from django.contrib.auth.models import User
from .validators import user_validator, password_validator


class RegisterForm(forms.ModelForm):
    password2 = forms.CharField(label=_('confirm password'), max_length=100, required=True,
                                widget=forms.PasswordInput(attrs={'class': 'form-control text-info'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control w-100'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control text-info'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'})
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        password_validator(password1, password2)
        return password2


class LoginForm(forms.Form):
    username = forms.CharField(label=_('Username'), max_length=150, required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control my- 2'}))
    password = forms.CharField(label=_('Password'), max_length=150, required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control my-2'}))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {'content': forms.Textarea(attrs={'class': 'form-control', 'style': 'resize:none;',
                                                    'rows': '10', 'cols': '80',
                                                    'placeholder': 'Enter your comment...'})}
