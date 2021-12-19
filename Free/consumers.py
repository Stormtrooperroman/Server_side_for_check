import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            "hello",
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            "hello",
            self.channel_name
        )

    def chat_message(self, event):
        message = event['message']
        status = event['status']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            "status": status
        }))