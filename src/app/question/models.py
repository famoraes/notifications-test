from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed

from app.notification.models import Notification, NOTIFICATION_TYPES


class Question(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="questions")
    title = models.CharField(max_length=100)
    content = models.TextField()
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="questions_liked")


def question_liked(sender, **kwargs):
    if kwargs['action'] == 'post_add':

        for user_pk in kwargs['pk_set']:
            user = User.objects.get(pk=user_pk)

            Notification.objects.create(
                user = kwargs['instance'].user,
                n_type = NOTIFICATION_TYPES['LIKE'],
                title = '{0} likes your question'.format(user.username),
                content = '{0} likes your question'.format(user.username),
                extra = {
                    'question_id': kwargs['instance'].id
                }
            )

m2m_changed.connect(question_liked, sender=Question.likes.through)
