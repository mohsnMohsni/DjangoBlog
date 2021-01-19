from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import Post, Comment, CommentLike, Category
from .forms import PostForm, EditPostForm
from .mixins import PostAuthorAccessMixin
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from account.mixins import AuthorAccessMixin
from django.db.utils import IntegrityError
import json


class PostsView(ListView):
    model = Post
    paginate_by = 10
    template_name = 'blog/Show/posts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.filter(parent=None)
        return context


class CategoryView(ListView):
    template_name = 'blog/Show/category.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        try:
            cat = Category.objects.get(title=self.kwargs.get('cat'))
            posts = Post.objects.filter(category=cat)
        except Category.DoesNotExist:
            posts = []
        return posts


class PostView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/Show/post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['setting'] = context.get('post').setting
        return context


class AddPostView(AuthorAccessMixin, CreateView):
    model = Post
    template_name = 'blog/Handle/add_post.html'
    form_class = PostForm

    def get_success_url(self):
        return reverse('blog:posts')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        p = Post.objects.get(slug=self.request.POST.get('slug'))
        p.create_setting()
        return HttpResponseRedirect(self.get_success_url())


class EditPostView(AuthorAccessMixin, PostAuthorAccessMixin, UpdateView):
    model = Post
    form_class = EditPostForm
    template_name = 'blog/Handle/edit_post.html'

    def get_success_url(self):
        return reverse('blog:post', kwargs={'slug': self.kwargs.get('slug')})


@csrf_exempt
def get_comments(request, slug):
    comments = Post.objects.get(slug=slug).get_comments()
    comments_dic = list()
    for parent, children in comments:
        children_list = list()
        for child in children:
            children_list.append({'author': child.author.full_name, 'content': child.content,
                                  'create_at': child.create_at, 'like_count': child.like_count,
                                  'dislike_count': child.dis_like_count, 'id': child.id})
        comments_dic.append({'author': parent.author.full_name, 'content': parent.content, 'id': parent.id,
                             'create_at': parent.create_at, 'like_count': parent.like_count,
                             'dislike_count': parent.dis_like_count, 'children': children_list})

    return JsonResponse(comments_dic, safe=False)


@csrf_exempt
def add_comment(request):
    data = json.loads(request.body)
    author = request.user
    if not author.is_authenticated:
        return HttpResponse('No Access', status=403)
    try:
        post = Post.objects.get(slug=data.get('slug'))
    except Post.DoesNotExist:
        return HttpResponse('Bad Request', status=404)
    try:
        parent = Comment.objects.get(pk=data.get('cm_parent'))
        Comment.objects.create(author=author, content=data.get('comment'), post=post, parent=parent)
    except (Comment.DoesNotExist, ValueError):
        Comment.objects.create(author=author, content=data.get('comment'), post=post)
    return HttpResponse('ok')


@csrf_exempt
def like_comment(request):
    data = json.loads(request.body)
    author = request.user
    if not author.is_authenticated:
        return HttpResponse('Not Access', status=403)
    try:
        cm = Comment.objects.get(pk=data.get('comment_id'))
    except Comment.DoesNotExist:
        return HttpResponse('Bad Request', status=404)
    try:
        CommentLike.objects.create(author=author, comment=cm, condition=data.get('condition'))
    except (CommentLike.DoesNotExist, IntegrityError):
        CommentLike.objects.filter(author=author, comment=cm).update(condition=data.get('condition'))

    return HttpResponse('ok')
