from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class User(AbstractUser):

    groups = models.ManyToManyField(Group)
    phone = models.CharField(unique=True, max_length=15, default=None, null=True)
    report_to = models.ForeignKey('self', on_delete=models.PROTECT, default=None, null=True, blank=True)

    def __str__(self):
        return self.username
