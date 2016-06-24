import json
import requests
from pusher import Pusher

from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField

NOTIFICATION_TYPES = {
    'LIKE': 'LIKE',
    'ANSWER': 'ANSWER',
    'FOLLOW': 'FOLLOW'
}

NOTIFICATION_CHOICES = (
    (NOTIFICATION_TYPES['LIKE'], NOTIFICATION_TYPES['LIKE']),
    (NOTIFICATION_TYPES['ANSWER'], NOTIFICATION_TYPES['ANSWER']),
    (NOTIFICATION_TYPES['FOLLOW'], NOTIFICATION_TYPES['FOLLOW'])
)


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    n_type = models.CharField(max_length=20, choices=NOTIFICATION_CHOICES, null=True)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=True)
    is_seen = models.BooleanField(default=False, db_index=True)
    extra = JSONField()

    def _get_user_channel(self):
        return "user-{0}".format(self.user.id)

    def save(self, **kwargs):
        from .serializers import NotificationSerializer

        super(Notification, self).save()
        data = NotificationSerializer(self).data
        pusher = Pusher(
            app_id=settings.PUSHER_APP_ID,
            key=settings.PUSHER_KEY,
            secret=settings.PUSHER_SECRET
        )

        pusher.trigger(self._get_user_channel(), 'notification', json.dumps(data))
