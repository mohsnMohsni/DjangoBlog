from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from blog.models import Post, Comment, User
from blog.forms import PostForm


@login_required
def add_post(request):
    if request.method == 'GET':
        form = PostForm()
    else:
        form = PostForm(request.POST)
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


def edit_post(request, slug):
    return
