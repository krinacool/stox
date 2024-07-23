# management/commands/load_instruments.py
import csv
import time
from django.core.management.base import BaseCommand
from app.orders.market import market_order

class Command(BaseCommand):
    help = 'Close Intraday Positions'

    def handle(self, *args, **kwargs):
        from app.models import Position,Order
        obj = Position.objects.filter(is_closed=False,product='Intraday')
        for i in obj:
            print(i.symbol)
            try:
                order_type = 'SELL'
                quantity = i.quantity
                if quantity < 0:
                    order_type = 'SELL'
                    quantity = quantity * -1
                market_order(i.user,i.symbol,i.instrument_key,i.token,quantity,order_type,i.product,0,0,'Market')
            except:
                pass
        
        ob = Order.objects.filter(status='pending').filter(type='Limit')
        for x in ob:
            ob.delete()
        self.stdout.write(self.style.SUCCESS('Closed Positions Successfully'))

