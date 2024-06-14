from django.urls import path
from app import consumers
from django.urls import re_path


websocket_urlpatterns = [
    re_path(r'ws/stocks/$', consumers.StockConsumer.as_asgi()),
    # path("ws/get_price/", consumers.PriceConsumer.as_asgi()),
    # path("ws/symbols/", consumers.SymbolList.as_asgi()),
]