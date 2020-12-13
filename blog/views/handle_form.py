from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from blog.models import Post, Comment, CommentLike
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


@login_required
def comment_like(request, cm_id):
    author = request.user
    cm = Comment.objects.get(pk=cm_id)
    like_status = request.POST.get('like_status')
    like_status = True if like_status == 'True' else False
    if CommentLike.objects.filter(author=author, comment=cm).exists():
        CommentLike.objects.filter(author=author, comment=cm).update(condition=like_status)
    else:
        CommentLike.objects.create(author=author, comment=cm, condition=like_status)
    return redirect('blog:post', slug='Cillum')
