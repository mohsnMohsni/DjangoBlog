from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from blog.forms import RegisterForm


def log_in(request):
    if request.user.is_authenticated:
        return redirect('blog:home')
    if request.method != 'POST':
        pass
    else:
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('blog:home')
    return render(request, 'blog/auth/login.html', context={})


def log_out(request):
    logout(request)
    return redirect('blog:home')


def register(request):
    if request.method != 'POST':
        form = RegisterForm()
    else:
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            user = User.objects.create(username=username, first_name=first_name,
                                       last_name=last_name, email=email)
            user.set_password(password)
            user.save()
            return redirect('blog:home')

    context = {
        'form': form
    }
    return render(request, 'blog/auth/register.html', context=context)
