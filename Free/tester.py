from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import time
def main():
    layer = get_channel_layer()
    async_to_sync(layer.group_send)("hello", {"type": "chat.message","message": "Hello there!",})


    async_to_sync(layer.group_send)("hello", {"type": "chat.message","message": "Hello man!",})
