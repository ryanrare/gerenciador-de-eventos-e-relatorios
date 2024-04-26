from .models import Notification, UserEventNotification, UserEvent
from notifications.consumers import active_consumers
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def send_notifications_to_users(title, type_notification, event, user):
    notification = Notification.objects.create(
        description=f"the {title} event you are registered for has been updated",
        type=f"{type_notification}"
    )
    event_data = {
        'title': title,
        'event_id': event.id,
        'notification_id': notification.id,
    }
    user_events = UserEvent.objects.filter(event=event)
    for user_event in user_events:
        UserEventNotification.objects.create(
            user_event=user_event,
            notification=notification,
            sent_by=user
        )

    for consumer in active_consumers:
        consumer.send(text_data=json.dumps(event_data))
