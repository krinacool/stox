# chating/asgi.py
import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

from app.routings import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stock.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
    }
)

