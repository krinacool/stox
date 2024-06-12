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
    