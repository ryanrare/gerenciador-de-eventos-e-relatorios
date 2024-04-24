from django.db import models
from users.models import User


class Notification(models.Model):
    TYPES = (
        ('canceled', 'Canceled'),
        ('update', 'Update'),
    )

    description = models.TextField()
    type = models.CharField(max_length=10, choices=TYPES)
    sent_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.get_type_display()}: {self.descrition}"


class UserNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}: {self.notification}"
