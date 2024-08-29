from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    用户模型
    """
    email = models.EmailField(u'邮箱地址', max_length=120, null=True, unique=True)