import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Event

class EventConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'events_group'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data.get('action') == 'update':
            events = await self.get_events()
            await self.channel_layer.group_send(
                self.room_group_name,
                {'type': 'send_events', 'events': events}
            )

    async def send_events(self, event):
        await self.send(text_data=json.dumps(event['events']))

    @database_sync_to_async
    def get_events(self):
        return list(Event.objects.all().values())