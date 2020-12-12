from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    title = models.CharField(_("Title"), max_length=50)
    slug = models.SlugField(_("Slug"), unique=True, db_index=True)
    parent = models.ForeignKey("self", verbose_name=_("Parent"), on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='children', related_query_name='children')

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.slug


class CommentLike(models.Model):
    author = models.ForeignKey(User, verbose_name=_(
        "Author"), on_delete=models.CASCADE)
    comment = models.ForeignKey('blog.Comment', verbose_name=_(
        'Comment'), on_delete=models.CASCADE, related_name="comment_like", related_query_name="comment_like")
    condition = models.BooleanField(_("Condition"))
    create_at = models.DateTimeField(_("Create at"), auto_now_add=True)
    update_at = models.DateTimeField(_("Update at"), auto_now=True)

    class Meta:
        unique_together = [['author', 'comment']]
        verbose_name = _("CommentLike")
        verbose_name_plural = _("CommentLikes")

    def __str__(self):
        return str(self.condition)


class Comment(models.Model):
    content = models.TextField(_("Content"))
    post = models.ForeignKey("Post", verbose_name=_("Post"),
                             on_delete=models.CASCADE,
                             related_name='comments', related_query_name='comments')
    create_at = models.DateTimeField(_("Create at"), auto_now_add=True)
    update_at = models.DateTimeField(_("Update at"), auto_now=True)
    author = models.ForeignKey(User, verbose_name=_(
        "Author"), on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(_("confirm"), default=True)
    parent = models.ForeignKey('self', verbose_name=_('parent'), null=True,
                               on_delete=models.CASCADE, blank=True,
                               related_name='children', related_query_name='child')

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ['-create_at']

    def __str__(self):
        return self.content[:10]

    @property
    def like_count(self):
        q = CommentLike.objects.filter(comment=self, condition=True)
        return q.count()

    @property
    def dis_like_count(self):
        q = CommentLike.objects.filter(comment=self, condition=False)
        return q.count()
