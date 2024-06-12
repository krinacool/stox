import csv
from app.orders.limit import place_limit_market_order

def process_limit_orders():
    file_path = 'limit_orders.csv'
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            instrument = row['instrument']
            order_id = row['order_id']
            order_type = row['order_type']
            slt = row['slt']
            ltp = float(row['ltp'])
            limit_price = float(row['limit_price'])
            if slt == 'False':
                if (order_type == 'BUY' and ltp <= limit_price):
                    place_limit_market_order(order_id)
                elif (order_type == 'SELL' and ltp >= limit_price):
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

process_limit_orders()