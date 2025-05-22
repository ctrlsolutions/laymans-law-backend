from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification

def create_notification(recipient, notification_type, title, message, related_object_id=None, related_object_type=None):
    """
    Create a notification and send it through WebSocket if the user is online.
    
    Args:
        recipient: User instance
        notification_type: Type of notification (from Notification.NOTIFICATION_TYPES)
        title: Notification title
        message: Notification message
        related_object_id: Optional ID of related object
        related_object_type: Optional type of related object
    """
    # Create notification in database
    notification = Notification.objects.create(
        recipient=recipient,
        notification_type=notification_type,
        title=title,
        message=message,
        related_object_id=related_object_id,
        related_object_type=related_object_type
    )

    # Send through WebSocket if user is online
    channel_layer = get_channel_layer()
    room_group_name = f"user_{recipient.user_id}_notifications"
    
    async_to_sync(channel_layer.group_send)(
        room_group_name,
        {
            'type': 'send_notification',
            'notification': {
                'id': notification.id,
                'type': notification.notification_type,
                'title': notification.title,
                'message': notification.message,
                'created_at': notification.created_at.isoformat(),
                'is_read': notification.is_read,
                'related_object_id': notification.related_object_id,
                'related_object_type': notification.related_object_type
            }
        }
    )
    
    return notification 