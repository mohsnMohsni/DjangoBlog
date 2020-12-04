from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
    username = forms.CharField(label=_('username'), max_length=200)
    email = forms.EmailField(label=_('email'), required=True, help_text=_('valid email for reset password'))
    password = forms.CharField(label=_('password'), widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label=_('confirm password'), widget=forms.PasswordInput, required=True)
    first_name = forms.CharField(label=_('first name'))
    last_name = forms.CharField(label=_('last name'))

    # def clean(self):
    #     password = self.cleaned_data.get('password')
    #     password2 = self.cleaned_data.get('password2')
    #
    #     if password != password2:
    #         raise forms.ValidationError(
    #             'passwords are not match'
    #         )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # user = User.objects.get(username=username, None)
        user = None
        if username[0] == int or username.__contains__(' ') or user is not None:
            raise forms.ValidationError(
                'username not valid'
            )
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 6:
            raise forms.ValidationError(
                'password is similar'
            )
        return password


