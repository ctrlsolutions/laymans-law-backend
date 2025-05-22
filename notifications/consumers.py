import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Notification

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            self.user_id = str(self.scope["user"].user_id)
            self.room_group_name = f"user_{self.user_id}_notifications"
            
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json.get('action')
        
        if action == 'mark_read':
            notification_id = text_data_json.get('notification_id')
            await self.mark_notification_as_read(notification_id)

    async def send_notification(self, event):
        """Send notification to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'notification': event['notification']
        }))

    @database_sync_to_async
    def mark_notification_as_read(self, notification_id):
        try:
            notification = Notification.objects.get(
                id=notification_id,
                recipient_id=self.user_id
            )
            notification.mark_as_read()
            return True
        except Notification.DoesNotExist:
            return False 