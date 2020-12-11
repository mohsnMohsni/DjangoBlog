from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
  email = models.EmailField(_('email'), blank=True, db_index=True)
  avatar = models.ImageField(_('avatar'), upload_to='user/avatar', blank=True)
