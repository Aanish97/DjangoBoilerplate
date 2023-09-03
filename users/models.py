from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True, blank=False, null=False)

    # token reset fields
    reset_password_token = models.CharField(max_length=100, blank=True, null=True)
    token_created_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.username)
