import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

from santri_app.dashboard.routing import websocket_urlpatterns

os.environ["DJANGO_READ_DOT_ENV_FILE"] = "True"
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

# import os
# import sys
# from urllib.parse import unquote

# from django.core.wsgi import get_wsgi_application

# sys.path.append(os.getcwd())
# os.environ["DJANGO_READ_DOT_ENV_FILE"] = "True"
# os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings.production"


# def application(environ, start_response):
#     environ["PATH_INFO"] = unquote(environ["PATH_INFO"]).encode("utf-8").decode("iso-8859-1")
#     _application = get_wsgi_application()
#     return _application(environ, start_response)
