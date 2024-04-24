from django.db import models
from users.models import User


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, null=True)
    update_at = models.DateField(null=True, blank=True)
    deleted_at = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'event'
        db_table = 'event'


class UserEvent(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    event = models.ForeignKey(Event, verbose_name="Event", on_delete=models.CASCADE)
    registration_date = models.DateTimeField("Registration Date", auto_now_add=True)

    class Meta:
        verbose_name = "user event"
        verbose_name_plural = "user events"
        db_table = "user_event"
