from .models import Notification, UserEventNotification, UserEvent
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync


def send_notifications_to_users(title, type_notification, event, user):
    notification = Notification.objects.create(
        description=f"the {title} event you are registered for has been updated",
        type=f"{type_notification}"
    )
    user_events = UserEvent.objects.filter(event=event)
    for user_event in user_events:
        UserEventNotification.objects.create(
            user_event=user_event,
            notification=notification,
            sent_by=user
        )
    # channel_layer = get_channel_layer()
    # async_to_sync(channel_layer.group_send)(
    #     'notifications_group',
    #     {
    #         'type': 'send_notification',
    #         'message': f"the {title} event you are registered for has been updated"
    #     }
    # )
