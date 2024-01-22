from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name=_("ایمیل"))
    user_password_rest_token = models.CharField(max_length=32, unique=True, verbose_name=_("توکن تغییر رمز عبور"),
                                                blank=True, null=True)
