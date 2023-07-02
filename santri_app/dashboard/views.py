from rest_framework.response import Response
from rest_framework.views import APIView

from santri_app.dashboard.consumers import GroupSend


class GroupSendView(APIView):
    def post(self, request, format=None):
        dashboard_id = request.data.get("id", None)
        message = request.data.get("message", None)

        if dashboard_id and message:
            group_name = f"dashboard_{dashboard_id}"
            sender = GroupSend()
            sender.send(group_name, message)

            return Response({"result": "Message sent"})
        else:
            return Response({"error": "Invalid data"})
