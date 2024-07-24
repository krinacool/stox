import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_helper import ShoonyaApiPy
import logging
import yaml
import pyotp
from settings.models import ShoonyaApi
#enable dbug to see request and responses
logging.basicConfig(level=logging.DEBUG)

#start of our program
def shoonya_order(obj):
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
    product_type = 'C'
    if obj.order_type == 'BUY':
        buy_or_sell = 'B'
    if obj.product == 'Intraday':
        product_type = 'I'
    try:
        from app.models import Shoonya_Instrument, Instrument
        token = Instrument.objects.filter(instrument_key=obj.instrument_key).first().exchange_token
        segment = 'NSE'
        if obj.segment == 'BSE_EQ':
            segment = 'BSE'
        elif obj.segment == 'BSE_FO':
            segment = 'BFO'
        elif obj.segment == 'NCD_FO':
            segment = 'CDS'
        elif obj.segment == 'MCX_FO':
            segment = 'MCX'
        elif obj.segment == 'NSE_FO':
            segment = 'NFO'
        elif obj.segment == 'NSE_EQ':
            segment = 'NSE'
        print('=-=-=-')
        print(token)
        print(obj.segment)
        print(segment)
        syb = Shoonya_Instrument.objects.all().filter(exchange=segment).filter(exchange_token=str(token)).first()
        print(syb.tradingsymbol)
        ret = api.place_order(buy_or_sell=buy_or_sell, product_type=product_type,
                                exchange=segment, tradingsymbol=syb.tradingsymbol, 
                                quantity=1, discloseqty=0,price_type='MKT', price=0, trigger_price=0,
                                retention='DAY', remarks='my_order_001')
        print('ret')
        print(ret)
        orderno = ret['norenordno']
        ret = api.single_order_history(orderno=orderno)
        from app.models import Shoonya_Orders
        Shoonya_Orders.objects.create(response=ret)
        for ord in ret:
            print('-=-=-=')
            print(f"{ord['qty']} prc: {ord['prc']} trgprc: {ord['trgprc']} {ord['rpt']}")
    except Exception as e:
        print('Error is')
        print(e)


# ret = api.modify_order(exchange='NSE', tradingsymbol='CANBK-EQ', orderno=orderno,
#                                    newquantity=2, newprice_type='SL-LMT', newprice=201.00, newtrigger_price=200.00)


# print(ret)

# ret = api.modify_order(exchange='NSE', tradingsymbol='CANBK-EQ', orderno=orderno,
#                                    newquantity=2, newprice_type='MKT', newprice=0.00)

# print(ret)




