import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

from santri_app.chat.routing import get_chat_websocket_url_patterns
from santri_app.dashboard.routing import get_dashboard_websocket_urlpatterns

websocket_urlpatterns = get_dashboard_websocket_urlpatterns() + get_chat_websocket_url_patterns()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(AuthMiddlewareStack(URLRouter(websocket_urlpatterns))),
    }
)
