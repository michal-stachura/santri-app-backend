import json
from urllib.parse import parse_qs

from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token


class GroupSend:
    def send(self, group_name, message):
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(group_name, message)


class ChatConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def __get_user(self, token):
        try:
            user_token = Token.objects.get(key=token)
            return user_token.user
        except Token.DoesNotExist:
            return AnonymousUser()

    async def connect(self):
        query_string = self.scope["query_string"].decode()
        params = parse_qs(query_string)
        token = params.get("token")

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        if not token:
            await self.close()
        else:
            token = token[0]
            user = await self.__get_user(token)

            if user.is_authenticated:
                self.scope["user"] = user
                await self.accept()
                # Join room group
                await self.channel_layer.group_add(self.room_group_name, self.channel_name)
                print(self.room_group_name)
                print(self.channel_name)
            else:
                await self.close()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(self.room_group_name, {"type": "chat.message", "message": message})

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to Websocket
        await self.send(text_data=json.dumps({"message": message}))
