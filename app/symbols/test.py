import re

def get_symbol(symbol):
    match = re.match(r'(.*?)(\d{2}[A-Z]{3}\d+)', symbol)
    if 'SENSEX' in symbol:
        return 'SENSEX'
    if match:
        result = match.group(1)
        return result
    else:
        return symbol
    
print(get_symbol('SENSEX2411969500PE'))