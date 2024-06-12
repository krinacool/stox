import csv
from data import get_price
import pandas as pd

def order_id_exists(order_id):
    if str(order_id).strip() == '':
        return True
    df = pd.read_csv('limit_orders.csv')
    instrument = df[df['order_id'] == order_id]
    if instrument.empty:
        return False
    else:
        return True

def limit_order(instrument,exchange,slt,limit_price,order_type,quantity,order_id):
    # INSTRUMENT #EXCHANGE #LTP #SLT
    ltp = get_price(instrument)
    if ltp is None:
        return ltp
    if order_id_exists(order_id):
        print('Already Exists')
        return None
    data_to_append = [instrument, exchange, ltp, slt, limit_price,order_type,quantity,order_id]
    csv_file_path = 'limit_orders.csv'
    with open(csv_file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data_to_append)
    return True


print(limit_order('OPPO','NSE',True,5000,'BUY',10,'new'))