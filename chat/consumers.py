import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.room_group_name = "test"
		await self.channel_layer.group_add(self.room_group_name, self.channel_name)
		await self.accept()
	
	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json["message"]
		await self.channel_layer.group_send(
			self.room_group_name,
			{
				"type": "chat_message",
				"message": message
			}
		)
	
	async def chat_message(self, event):
		message = event["message"]
		await self.send(text_data=json.dumps({
			"type": "chat",
			"message": message
		}))

		