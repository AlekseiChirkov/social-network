from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=64, unique=True)
    first_name = models.CharField(max_length=128, blank=True)
    last_name = models.CharField(max_length=128, blank=True)
    phone = models.CharField(max_length=128, blank=True, unique=True)
    email = models.EmailField(
        max_length=128, blank=True, null=True, unique=True
    )
    last_activity = models.DateTimeField(null=True)

    def __str__(self):
        return self.first_name
