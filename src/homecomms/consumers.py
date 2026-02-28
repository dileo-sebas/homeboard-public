import logging
from channels.generic.websocket import AsyncJsonWebsocketConsumer

class PracticeConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.temperature_group_name = "temperature"

        await self.channel_layer.group_add(
            self.temperature_group_name,
            self.channel_name
        )
        logging.info("Added to group temperature.")

        await self.accept()

    async def disconnect(self, message):
        await self.channel_layer.group_discard(
            self.temperature_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        logging.info(f"Received {text_data}")
        if text_data == 'PING':
            await self.send('PONG')

    async def temperature_reading(self, content, type="temperature_reading"):
        await self.send_json(content["message"].toJSON())