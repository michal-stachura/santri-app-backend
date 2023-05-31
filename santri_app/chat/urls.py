from django.urls import path

from santri_app.chat.views import index, room

urlpatterns = [path("", index, name="index"), path("<str:room_name>/", room, name="room")]
