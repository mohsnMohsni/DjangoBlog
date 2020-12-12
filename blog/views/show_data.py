from django.shortcuts import render, redirect
from blog.models import Post, Comment, User
from blog.forms import CommentForm


def home(request):
    return render(request, 'blog/home.html')


def posts(request):
    posts_all = Post.objects.all()
    context = {
        'posts': posts_all,
    }
    return render(request, 'blog/posts.html', context=context)


def post(request, slug):
    post_single = Post.objects.select_related('setting', 'author').get(slug=slug)
    author = User.objects.get(email=request.user.email)
    comments = Comment.objects.filter(post=post_single)
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        form = form.save(commit=False)
        form.post = post_single
        form.author = author
        form.save()
        return redirect('blog:post', slug=slug)
    context = {
        'post': post_single,
        'setting': post_single.setting,
        'comments': comments,
        'form': form,
    }
    return render(request, 'blog/post.html', context=context)
