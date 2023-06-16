import json

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
    def __get_user(self):
        try:
            user_token = Token.objects.get(key=self.dashboard_id)
            user = user_token.user
            return user
        except Token.DoesNotExist:
            return AnonymousUser()

    async def __set_dashboard_group(self, token):
        self.dashboard_id = token
        self.dashboard_group_name = f"dashboard_{self.dashboard_id}"

        user = await self.__get_user()
        if user.is_authenticated:
            self.scope["user"] = user
            await self.channel_layer.group_add(self.dashboard_group_name, self.channel_name)
        else:
            print("close connection")
            self.close()

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.dashboard_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)

        if "token" in data:
            # Triggered by dashboardSocket.value.onopen
            await self.__set_dashboard_group(data["token"])

        # Send to dashboard group
        await self.channel_layer.group_send(
            self.dashboard_group_name,
            {"type": "dashboard.message", "data": data},
        )

    # Receive message from dashboard group
    async def dashboard_message(self, event):
        # Send message to Websocket
        await self.send(text_data=json.dumps(event))
