from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from blog.forms import RegisterForm, LoginForm

User = get_user_model()


def log_in(request):
    if request.user.is_authenticated:
        return redirect('blog:home')
    if request.method != 'POST':
        form = LoginForm()
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('blog:home')

    context = {
        'form': form,
    }
    return render(request, 'blog/auth/login.html', context=context)


def log_out(request):
    logout(request)
    return redirect('blog:home')


def register(request):
    if request.method == 'GET':
        form = RegisterForm()
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            form.save()
            return redirect('blog:home')

    context = {
        'form': form,
    }
    return render(request, 'blog/auth/register.html', context=context)
