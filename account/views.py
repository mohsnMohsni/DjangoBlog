from django.shortcuts import redirect, reverse
from .forms import RegisterForm, LoginForm
from django.contrib.auth import get_user_model
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LogoutView, LoginView
from django.views.generic import ListView
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import Group
from .mixins import AuthorAccessMixin
from blog.models import Post

User = get_user_model()


class SingInView(LoginView):
    template_name = 'account/auth/login.html'
    redirect_authenticated_user = True
    form_class = LoginForm

    def get_success_url(self):
        if self.request.user.groups.filter(name='author').exists() or self.request.user.is_superuser:
            return reverse('account:profile')
        else:
            return reverse('blog:home')


class SignOutView(LogoutView):
    template_name = 'blog/home.html'


class SignUpView(CreateView):
    template_name = 'account/auth/register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        group = Group.objects.get(name='normal user')
        obj = form.save(commit=False)
        password = obj.password
        obj.set_password(obj.password)
        obj.save()
        obj.groups.add(group)
        user = authenticate(self.request, username=obj.email, password=password)
        if user:
            login(self.request, user)
        return redirect('blog:home')


class ProfileView(AuthorAccessMixin, ListView):
    template_name = 'account/profile/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_count'] = sum([p.comment_count for p in context['posts']])
        context['draft_count'] = Post.objects.filter(author=self.request.user, draft=True).count()
        return context
