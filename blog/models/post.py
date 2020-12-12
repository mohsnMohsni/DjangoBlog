from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    title = models.CharField(_("Title"), max_length=128)
    slug = models.SlugField(_("Slug"), db_index=True, unique=True)
    content = models.TextField(_("Content"))
    create_at = models.DateTimeField(_("Create at"), auto_now_add=True)
    update_at = models.DateTimeField(_("Update at"), auto_now=True)
    publish_time = models.DateTimeField(_("Publish at"), db_index=True)
    draft = models.BooleanField(_("Draft"), default=True, db_index=True)
    image = models.ImageField(
        _("image"), upload_to='images/', null=True, blank=True)
    category = models.ForeignKey("Category", verbose_name=_(
        "Category"), on_delete=models.CASCADE, null=True, blank=True)
    author = models.ForeignKey(User, verbose_name=_("Author"), on_delete=models.CASCADE,
                               related_name="posts", related_query_name="children",
                               )

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ['-publish_time']

    def __str__(self):
        return self.title

    def create_setting(self):
        return PostSetting.objects.create(post=self)

    @property
    def comment_count(self):
        q = self.comments.all()
        return q.count()

    @property
    def convert_publish_date(self):
        converted_date = f"{self.publish_time.day} - {self.publish_time.month} - {self.publish_time.year}"
        return converted_date

    @property
    def convert_create_date(self):
        converted_date = f"{self.create_at.day} - {self.create_at.month} - {self.create_at.year}"
        return converted_date


class PostSetting(models.Model):
    post = models.OneToOneField(
        "Post", verbose_name=_("post"), on_delete=models.CASCADE,
        related_name='setting', related_query_name='setting')
    comment = models.BooleanField(_("comment"), default=True)
    author = models.BooleanField(_("author"), default=False)
    allow_discussion = models.BooleanField(_("allow discussion"), default=False)

    class Meta:
        verbose_name = _("PostSetting")
        verbose_name_plural = _("PostSettings")
