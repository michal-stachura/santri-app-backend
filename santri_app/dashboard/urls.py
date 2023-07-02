from django.urls import path

from santri_app.dashboard.views import GroupSendView

urlpatterns = [
    path("group-send", GroupSendView.as_view(), name="group-send"),
]
