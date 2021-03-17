from django.db import models
from django.contrib.auth.models import User
from papermanager.models import Paper


class Link(models.Model):
    from_user = models.ForeignKey(User, models.CASCADE, related_name="from_user")
    to_user = models.ManyToManyField(User, blank=True, related_name="to_user")
    papers = models.ManyToManyField(Paper, blank=True)
