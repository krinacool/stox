from django.urls import path
from app import consumers

websocket_urlpatterns = [
    path("ws/get_price/", consumers.PriceConsumer.as_asgi()),
    path("ws/symbols/", consumers.SymbolList.as_asgi()),
]