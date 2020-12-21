from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post


class PostAuthorAccessMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        p = Post.objects.get(slug=kwargs.get('slug'))
        if request.user.is_authenticated and p.author == request.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            return self.handle_no_permission()
