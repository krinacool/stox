import pandas as pd
from stock.settings import SYMBOLS_FILE
import csv

def get_instrument(exchange_token):
    if str(exchange_token).strip() == '':
        return None
    exchange_token = float(exchange_token)
    df = pd.read_csv(SYMBOLS_FILE)
    instrument = df[df['exchange_token'] == exchange_token]
    if instrument.empty:
        return None
    else:
        return instrument.iloc[0]['instrument_key']
    
def get_instrument_type(exchange_token):
    if str(exchange_token).strip() == '':
        return None
    exchange_token = float(exchange_token)
    df = pd.read_csv(SYMBOLS_FILE)
    instrument = df[df['exchange_token'] == exchange_token]
    if instrument.empty:
        return None
    else:
        return instrument.iloc[0]['instrument_type']


def get_exchange(token):
    csv_file = 'syb.csv'  # Path to your CSV file
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if int(row['token']) == token:
                return row['exch_seg']
    return None



def get_symbol(token):
    csv_file = 'syb.csv'  # Path to your CSV file
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if int(row['token']) == token:
                return row['symbol']
    return None
    

def get_token(instrument_key):
    if str(instrument_key).strip() == '':
        return None
    df = pd.read_csv(SYMBOLS_FILE)
    instrument = df[df["instrument_key"] == instrument_key]
    if instrument.empty:
        return None
    else:
        return instrument.iloc[0]["exchange_token"]


# Example usage:

# df = pd.read_csv(SYMBOLS_FILE)
# # for x in df['exchange_token']:
# if 'USDINR2421680.1CE' in df['exchange_token']: