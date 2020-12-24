from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, reverse
from django.views.decorators.csrf import csrf_exempt
from .models import Post, Comment, CommentLike, Category
from .forms import PostForm, EditPostForm, CommentForm
from .mixins import PostAuthorAccessMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, FormView
from account.mixins import AuthorAccessMixin
import json


class HomeView(TemplateView):
    template_name = 'blog/Show/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.filter(parent=None)
        print(context['category'])
        return context


class PostsView(ListView):
    model = Post
    paginate_by = 4
    template_name = 'blog/Show/posts.html'


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
        cm_parent = None
        if self.request.GET.get('parent'):
            cm_parent = Comment.objects.get(pk=int(self.request.GET.get('parent')))
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['parent'] = cm_parent
        context['setting'] = context.get('post').setting
        context['comments'] = context.get('post').get_comments()
        return context


class AddCommentView(CreateView):
    model = Comment
    fields = ('content',)

    def get_success_url(self):
        return reverse('blog:post', kwargs={'slug': self.kwargs.get('slug')})

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.post = Post.objects.get(slug=self.request.POST.get('post'))
        if self.request.POST.get('parent'):
            obj.parent = Comment.objects.get(pk=int(self.request.POST.get('parent')))
        return super().form_valid(form)


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


# class CommentLikeView(LoginRequiredMixin, FormView):
#
#     def post(self, request, *args, **kwargs):
#         author = request.user
#         cm = Comment.objects.get(pk=request.POST.get('cm_id'))
#         like_status = request.POST.get('like_status')
#         like_status = True if like_status == 'True' else False
#         if CommentLike.objects.filter(author=author, comment=cm).exists():
#             CommentLike.objects.filter(author=author, comment=cm).update(condition=like_status)
#         else:
#             CommentLike.objects.create(author=author, comment=cm, condition=like_status)
#         return redirect('blog:post', slug=kwargs.get('slug'))


@csrf_exempt
def like_comment(request):
    data = json.loads(request.body)
    author = request.user
    try:
        cm = Comment.objects.get(pk=data['comment_id'])
    except Comment.DoesNotExist:
        return HttpResponse('Bad Request', status=404)
    cm_like = CommentLike.objects.filter(author=author, comment=cm)
    if cm_like.exists():
        cm_like.update(condition=data['condition'])
    else:
        CommentLike.objects.create(author=author, comment=cm, condition=data['condition'])

    return HttpResponse('ok')


def get_comment(request):
    return HttpResponse()
