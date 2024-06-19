import csv
import re

def get_symbol(symbol):
    if 'SENSEX' in symbol:
        return 'SENSEX'
    match = re.match(r'(.*?)(\d{2}[A-Z]{3}\d+)', symbol)
    if match:
        result = match.group(1)
        return result
    else:
        return symbol
    
def get_instrument_key(tradingsymbol, exchange):
    filename = 'complete.csv'
    with open(filename, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if (row['tradingsymbol'] == tradingsymbol or (not row['tradingsymbol'] and row['name'] == tradingsymbol)) and row['exchange'] == exchange:
                return row['instrument_key']
    return None