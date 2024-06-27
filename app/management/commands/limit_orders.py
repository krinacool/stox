# management/commands/load_instruments.py
import csv
import time
from django.core.management.base import BaseCommand
from settings.timing import market_open
from app.orders.market import market_order

class Command(BaseCommand):
    help = 'Execute Limit Orders'

    def handle(self, *args, **kwargs):
        from app.models import Order,symbols
        while True:
            obj = Order.objects.filter(status='pending').filter(type='Limit')
            for i in obj:
                if not market_open(i.segment):
                    return False
                    # return JsonResponse({'success': False, 'message': 'Market Closed'})
                price = symbols.objects.filter(instrument_key=i.instrument_key).first().ltp
                if (
                    (i.order_type == 'BUY' and int(price) == int(i.price)) or
                    (i.order_type == 'SELL' and int(price) == int(i.price))
                ):
                    market_order(i.user,i.symbol,i.instrument_key,00,i.quantity,i.order_type,i.product,i.stoploss,i.target,i.type)
                    i.delete()
            time.sleep(1)
            self.stdout.write(self.style.SUCCESS('Executed Orders Successfully'))
