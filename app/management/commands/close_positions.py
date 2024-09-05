# management/commands/load_instruments.py
import csv
import time
from django.core.management.base import BaseCommand
from app.orders.market import market_order
from settings.models import mcx_market_time, nse_market_time
import datetime
from django.utils import timezone

def market_time(segment):
    market_setting = ''
    if segment.upper() == 'MCX_FO':
        market_setting = mcx_market_time.objects.first()
    else:
        print('1')
        market_setting = nse_market_time.objects.first()
        print(datetime.datetime.now().time())
        print(market_setting.position_close_time)
    if datetime.datetime.now().time() > market_setting.position_close_time:
        print('2')
        return True
    else:
        return False

def market_open(segment):
    market_setting = ''
    if segment.upper() == 'MCX_FO':
        market_setting = mcx_market_time.objects.first()
    else:
        print('hello')
        market_setting = nse_market_time.objects.first()
    market_dates = market_setting.market_dates.all()
    today = timezone.now().date().day
    if market_time(segment):
        print('hello')
        for x in market_dates:
            if str(today) == str(x):
                return True
        return False
    else:
        return False

class Command(BaseCommand):
    help = 'Close Intraday Positions'

    def handle(self, *args, **kwargs):
        from app.models import Position,Order
        obj = Position.objects.filter(is_closed=False,product='Intraday')
        for i in obj:
            if market_open(i.segment):
                try:
                    order_type = 'SELL'
                    quantity = i.quantity
                    if quantity < 0:
                        order_type = 'SELL'
                        quantity = quantity * -1
                    market_order(i.user,i.symbol,i.instrument_key,i.token,quantity,order_type,i.product,0,0,'Market',True)
                except:
                    pass
            ob = Order.objects.filter(status='pending').filter(type='Limit')
            for x in ob:
                if market_open(x.segment):
                    ob.delete()
            self.stdout.write(self.style.SUCCESS('Closed Positions Successfully'))

