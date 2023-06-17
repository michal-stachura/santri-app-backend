from django.urls import re_path


def get_chat_websocket_url_patterns():
    from . import consumers

    return [
        re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
    ]
