from django.db import models
from django.contrib.auth.models import Group


class Register(models.Model):
    username = models.CharField(max_length=18)
    password = models.CharField(max_length=80)
    bio = models.CharField(max_length=64)
    group = models.ManyToManyField(Group)
