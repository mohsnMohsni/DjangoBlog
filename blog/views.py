from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models
from django.contrib.auth import authenticate, login, logout


def home(request):
    return render(request, 'blog/home.html')


def posts(request):
    posts_all = models.Post.objects.all()
    context = {
        'posts': posts_all,
    }
    return render(request, 'blog/posts.html', context=context)


def post(request, slug):
    # post = get_object_or_404(models.Post)
    post_single = models.Post.objects.select_related('setting', 'author').get(slug=slug)
    context = {
        'post': post_single,
        'setting': post_single.setting,
    }
    return render(request, 'blog/post.html', context=context)


def category(request):
    catagory_all = models.Category.objects.all()
    return HttpResponse('')


def log_in(request):
    if request.user.is_authenticated:
        return redirect('blog:home')
    if request.method != 'POST':
        pass
    else:
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(request, username=username, password=password)
        print(username)
        print(password)
        print(user)
        if user:
            login(request, user)
            return redirect('blog:home')
    return render(request, 'blog/login.html', context={})


def log_out(request):
    logout(request)
    return redirect('blog:home')
