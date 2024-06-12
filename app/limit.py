import requests
from models import Order
from symbols.details import get_price
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stock.settings")

def limit_orders():
    obj = Order.objects.filter(status='pending').filter(type='LIMIT')
    for i in obj:
            # if not market_open(i.segment):
            #      return False
                # return JsonResponse({'success': False, 'message': 'Market Closed'})
            if (
                (i.order_type == 'BUY' and get_price(i.symbol) <= i.price) or
                (i.order_type == 'SELL' and get_price(i.symbol) >= i.price)
            ):
                market_order(i.user,i.symbol,i.quantity,i.order_type,i.product,i.stoploss,i.target,i.type)
                i.delete()
    return True

while True:
    limit_orders()