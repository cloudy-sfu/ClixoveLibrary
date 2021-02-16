from django.contrib.auth.models import User
from django.db import models
from papermanager.models import Paper


class ShareLink(models.Model):
    user_from = models.ForeignKey(User, on_delete=models.CASCADE)
    users_to = models.ManyToManyField(User, related_name='+')
    papers = models.ManyToManyField(Paper)
