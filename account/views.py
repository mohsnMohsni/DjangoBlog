from django.http import HttpResponse
from django.shortcuts import redirect, reverse, render
from .forms import RegisterForm, LoginForm
from django.contrib.auth import get_user_model
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LogoutView, LoginView
from django.views.generic import ListView
from django.contrib.auth import login
from django.contrib.auth.models import Group
from .mixins import AuthorAccessMixin
from blog.models import Post
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import ugettext_lazy as _

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
    template_name = 'blog/Show/home.html'


class SignUpView(CreateView):
    template_name = 'account/auth/register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        group = Group.objects.get(name='normal user')
        obj = form.save(commit=False)
        obj.set_password(obj.password)
        obj.save()
        obj.groups.add(group)
        current_site = get_current_site(self.request)
        mail_subject = _('Activate your SimpleBlog account.')
        message = render_to_string('account/auth/active_email.html', {
            'user': obj,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(obj.pk)),
            'token': account_activation_token.make_token(obj),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return render(self.request, 'account/auth/send_mail_response.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('blog:home')
    else:
        return HttpResponse(_('Activation link is invalid!'))


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
