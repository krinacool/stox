import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_helper import ShoonyaApiPy
import logging
import yaml
import pyotp
from settings.models import ShoonyaApi
import time
# #enable dbug to see request and responses
# logging.basicConfig(level=logging.DEBUG)

#start of our program
def shoonya_order(order_type,product,getsegment,instrument_key,quantity,price):
    api = ShoonyaApiPy()
    app = ShoonyaApi.objects.all().first()
    user = app.user
    token = app.token
    totp = pyotp.TOTP(token)
    factor2 = totp.now()
    vc = app.vendor_code
    apikey = app.api_key
    pwd = app.password
    imei = ''
    ret = api.login(userid = user, password = pwd, twoFA=factor2, vendor_code=vc, api_secret=apikey, imei=imei)
    buy_or_sell = 'S'
    product_type = 'I'
    if order_type == 'BUY':
        buy_or_sell = 'B'
    if product == 'Carryforward':
        if getsegment == 'BSE_FO' or getsegment == 'NSE_FO':
            product_type = 'M'
        else:
            product_type = 'C'
    try:
        from app.models import Shoonya_Instrument, Instrument
        token = Instrument.objects.filter(instrument_key=instrument_key).first().exchange_token
        segment = 'NSE'
        prctyp = 'MKT'
        if getsegment == 'BSE_EQ':
            segment = 'BSE'
        elif getsegment == 'BSE_FO':
            segment = 'BFO'
            prctyp = 'LMT'
        elif getsegment == 'NCD_FO':
            segment = 'CDS'
        elif getsegment == 'MCX_FO':
            segment = 'MCX'
        elif getsegment == 'NSE_FO':
            prctyp = 'LMT'
            segment = 'NFO'
        elif getsegment == 'NSE_EQ':
            segment = 'NSE'
        print('=-=-=-')
        print(token)
        print(segment)
        print(segment)
        syb = Shoonya_Instrument.objects.all().filter(exchange=segment).filter(exchange_token=str(token)).first()
        print(syb.tradingsymbol)
        ret = api.place_order(buy_or_sell=buy_or_sell, product_type=product_type,
                                exchange=segment, tradingsymbol=syb.tradingsymbol, 
                                quantity=quantity, discloseqty=0,price_type=prctyp, price=price, trigger_price=0,
                                retention='DAY', remarks='Onstock')
        print('ret')
        print(ret)
        from app.models import Shoonya_Orders
        orderno = ret['norenordno']
        if prctyp == 'LMT':
            Shoonya_Orders.objects.create(response=ret)
            return price
        time.sleep(4)
        ret = api.single_order_history(orderno=orderno)
        Shoonya_Orders.objects.create(response=ret)
        return ret[0]['avgprc']
    except Exception as e:
        return None


# ret = api.modify_order(exchange='NSE', tradingsymbol='CANBK-EQ', orderno=orderno,
#                                    newquantity=2, newprice_type='SL-LMT', newprice=201.00, newtrigger_price=200.00)


# print(ret)

# ret = api.modify_order(exchange='NSE', tradingsymbol='CANBK-EQ', orderno=orderno,
#                                    newquantity=2, newprice_type='MKT', newprice=0.00)

# print(ret)




