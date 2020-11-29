from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from . import models


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
