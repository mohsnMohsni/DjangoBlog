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
    author = User.objects.get(email=request.user.email) if request.user.is_authenticated else None
    form = CommentForm()
    parent = request.GET.get('parent', -1)
    try:
        parent_exist = Comment.objects.get(id=int(parent))
    except Comment.DoesNotExist:
        parent_exist = None
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        form = form.save(commit=False)
        form.post = post_single
        form.author = author
        if parent and parent_exist:
            form.parent = parent_exist
        form.save()
        return redirect('blog:post', slug=slug)
    context = {
        'post': post_single,
        'parent': parent_exist,
        'setting': post_single.setting,
        'comments': post_single.get_comments(),
        'form': form,
    }
    return render(request, 'blog/post.html', context=context)
