from app.symbols.details import get_price
import pandas as pd
import csv
from stock.settings import LIMIT_ORDERS_FILE

def place_limit_market_order(order_id):
    from app.orders.market import market_order
    from app.symbols.instruments import get_token
    from app.models import Order
    try:
        ord = Order.objects.filter(order_id=order_id,status='pending').first()
        token = get_token(ord.instrument_key)
        market_order(ord.user,ord.symbol,ord.instrument_key,token,ord.quantity,ord.order_type,ord.product,ord.stoploss,ord.target,type='LIMIT')
        ord.delete()
    except:
        pass


def order_id_exists(order_id):
    if str(order_id).strip() == '':
        return True
    df = pd.read_csv(LIMIT_ORDERS_FILE)
    instrument = df[df['order_id'] == order_id]
    if instrument.empty:
        return False
    else:
        return True

def new_limit_order(order_id,slt=False):
    from app.models import Order
    print('NEW LIMIT ORDER')
    ord = Order.objects.get(order_id=order_id)
    instrument = ord.instrument_key
    exchange = ord.segment
    limit_price = ord.price
    order_type = ord.order_type
    quantity = ord.quantity
    ltp = get_price(instrument)
    if ltp is None:
        return ltp
    if order_id_exists(order_id):
        print('Already Exists')
        return None
    data_to_append = [instrument, exchange, ltp, slt, limit_price,order_type,quantity,order_id]
    csv_file_path = LIMIT_ORDERS_FILE
    with open(csv_file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data_to_append)
    return True

def initiate_limit_order(user,symbol,instrument_key,token,price,quantity,order_type,product,stoploss,target,slt=False):
    from app.models import Order
    from app.symbols.instruments import get_exchange
    print('AA GYE')
    amount = float(price) * int(quantity)
    print(price)
    print(quantity)
    print('AMOUNT')
    print(amount)
    segment = get_exchange(token)
    ord = Order.objects.create(user=user,symbol=symbol,instrument_key=instrument_key,segment=segment,price=price,amount=amount,quantity=quantity,order_type=order_type,product=product,status="pending",type='LIMIT',stoploss=stoploss,target=target)
    print(new_limit_order(ord.order_id,slt))
