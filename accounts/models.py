from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.mangers import UserManager


# Create your models here.

class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to="avatars/", default="avatars/default.jpg")
    mobile_number = models.CharField()
    country = models.CharField()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
