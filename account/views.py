from django.shortcuts import redirect
from .forms import RegisterForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LogoutView, LoginView

User = get_user_model()


class SingInView(LoginView):
    template_name = 'auth/login.html'
    redirect_authenticated_user = True
    form_class = AuthenticationForm


class SignOutView(LogoutView):
    template_name = 'blog/home.html'


class SignUpView(CreateView):
    template_name = 'auth/register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.set_password(obj.password)
        obj.save()
        return redirect('blog:home')
