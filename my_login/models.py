from django.db import models

from django.contrib.auth.models import Group, User


class Register(models.Model):
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    bio = models.TextField(blank=True)
    group = models.ForeignKey(Group, models.CASCADE, null=True)

    def __str__(self):
        return self.username
