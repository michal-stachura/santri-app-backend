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


class DashboardConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def __get_user(self, email):
        try:
            user_token = Token.objects.get(key=self.dashboard_id)
            user = user_token.user
            return user if user.email == email else AnonymousUser()
        except Token.DoesNotExist:
            return AnonymousUser()

    async def connect(self):
        query_string = self.scope["query_string"].decode()
        params = parse_qs(query_string)
        email = params.get("email", None)

        self.dashboard_id = self.scope["url_route"]["kwargs"]["token"]
        self.dashboard_group_name = f"dashboard_{self.dashboard_id}"

        if not email:
            await self.close()
        else:
            email = email[0]
            user = await self.__get_user(email)
            if user.is_authenticated:
                self.scope["user"] = user
                await self.accept()
                await self.channel_layer.group_add(self.dashboard_group_name, self.channel_name)
            else:
                await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.dashboard_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]

        # Send to dashboard group
        await self.channel_layer.group_send(
            self.dashboard_group_name, {"type": "dashboard.message", "message": message}
        )

    # Receive message from dashboard group
    async def dashboard_message(self, event):
        message = event["message"]

        # Send message to Websocket
        await self.send(text_data=json.dumps({"message": message}))
