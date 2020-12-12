from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from blog.models import Post
from blog.forms import PostForm, EditPostForm


@login_required
def add_post(request):
    if request.method == 'GET':
        form = PostForm()
    else:
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            slug = form.cleaned_data.get('slug')
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            p = Post.objects.get(slug=slug)
            p.create_setting()
            return redirect('blog:posts')
    context = {
        'form': form
    }
    return render(request, 'blog/add_post.html', context=context)


@login_required
def edit_post(request, slug):
    p = Post.objects.select_related('setting').get(slug=slug)
    if request.user != p.author:
        return redirect('blog:home')
    if request.method == 'GET':
        form = EditPostForm(instance=p)
    else:
        form = EditPostForm(request.POST, instance=p)
        if form.is_valid():
            form.save()
            return redirect('blog:posts')
    context = {
        'form': form,
    }
    return render(request, 'blog/edit_post.html', context=context)
