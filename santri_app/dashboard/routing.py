from django.urls import path


def get_websocket_urlpatterns():
    from . import consumers

    return [
        path("ws/dashboard/", consumers.DashboardConsumer.as_asgi()),
    ]
