from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateField()
    update_at = models.DateField()
    deleted_at = models.DateField()
    location = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'event'
        db_table = 'event'
