from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class User(AbstractUser):

    groups = models.ForeignKey(Group, on_delete=models.CASCADE, default=None, null=True)
    contact = models.CharField(unique=True, max_length=15)

    def __str__(self):
        return self.username
