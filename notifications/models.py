from django.db import models
from users.models import User
from events.models import UserEvent
from django.utils import timezone


class Notification(models.Model):
    TYPES = (
        ('canceled', 'Canceled'),
        ('update', 'Update'),
    )

    description = models.TextField()
    type = models.CharField(max_length=10, choices=TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'notification'


class UserEventNotification(models.Model):
    user_event = models.ForeignKey(UserEvent, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    sent_at = models.DateTimeField(default=timezone.now)
    sent_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_event_notification'
