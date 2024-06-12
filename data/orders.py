import csv
# from app.orders.limit import place_limit_market_order
from threading import Thread
import time

def place_limit_market_order(order_id):
    print('Orders placed')
    print(order_id)

ORDERS_FILE = 'C:\\Users\\atulg\\Desktop\\stock\\data\\limit_orders.csv'

def process_limit_orders():
    file_path = ORDERS_FILE
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            instrument = row['instrument']
            print(instrument)
            order_id = row['order_id']
            order_type = row['order_type']
            slt = row['slt']
            ltp = float(row['ltp'])
            limit_price = float(row['limit_price'])
            if slt == 'False':
                print('STOPLOSS IS NOT HERE')
                if (order_type == 'BUY' and ltp >= limit_price):
                    print('BUY HERE')
                    place_limit_market_order(order_id)
                    print('placed')
                elif (order_type == 'SELL' and ltp <= limit_price):
                    place_limit_market_order(order_id)
            elif slt == 's':
                if (order_type == 'BUY' and ltp >=limit_price):
                    place_limit_market_order(order_id)
                if (order_type == 'SELL' and ltp <= limit_price):
                    place_limit_market_order(order_id)
            elif slt == 't':
                if(order_type == 'BUY' and ltp <= limit_price):
                    place_limit_market_order(order_id)
                elif(order_type == 'SELL' and ltp >= limit_price):
                    place_limit_market_order(order_id)

def task():
    print('-=-=-=-=STARTED-=-=-=-=-=')
    while True:
        print('processing')
        process_limit_orders()
        time.sleep(5)

task()



