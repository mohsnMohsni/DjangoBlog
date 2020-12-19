from django import forms
from django.contrib.auth.forms import UsernameField, UserModel
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils.text import capfirst
from django.contrib.auth import authenticate, get_user_model
from .validators import password_validator, fullname_validator

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


class AuthenticationForm(forms.Form):
    username = UsernameField(label=_("Email"), widget=forms.TextInput(
        attrs={'autofocus': True, 'class': 'form-control my- 2'}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
                                          'class': 'form-control my- 2'}),
    )

    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        username_max_length = self.username_field.max_length or 254
        self.fields['username'].max_length = username_max_length
        self.fields['username'].widget.attrs['maxlength'] = username_max_length
        if self.fields['username'].label is None:
            self.fields['username'].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'username': self.username_field.verbose_name},
        )
