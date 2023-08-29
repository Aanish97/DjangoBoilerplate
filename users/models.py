from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True, blank=False, null=False)

    def __str__(self):
        return str(self.username)
