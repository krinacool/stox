from settings.models import nse_market_time,mcx_market_time
from django.utils import timezone
import datetime


def market_time(segment):
    market_setting = ''
    if segment.upper() == 'MCX_FO':
        market_setting = mcx_market_time.objects.first()
    else:
        print('1')
        market_setting = nse_market_time.objects.first()
        print(datetime.datetime.now().time())
        print(market_setting.close_time)
    if datetime.datetime.now().time() < market_setting.close_time and datetime.datetime.now().time() > market_setting.open_time:
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