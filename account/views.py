from django.shortcuts import redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth import get_user_model
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth import login, authenticate

User = get_user_model()


class SingInView(LoginView):
    template_name = 'auth/login.html'
    redirect_authenticated_user = True
    form_class = LoginForm


class SignOutView(LogoutView):
    template_name = 'blog/home.html'


class SignUpView(CreateView):
    template_name = 'auth/register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        password = obj.password
        obj.set_password(obj.password)
        obj.save()
        user = authenticate(self.request, username=obj.email, password=password)
        if user:
            login(self.request, user)
        return redirect('blog:home')
