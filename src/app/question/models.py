from django.db import models
from django.conf import settings


class Question(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="questions")
    title = models.CharField(max_length=100)
    content = models.TextField()
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="questions_liked")
