from stock.settings import DATA_FILE
import pandas as pd
import logging
from app.symbols.instruments import get_symbol
from settings.models import Upstox
logging.basicConfig(filename='log.txt', level=logging.ERROR, format='%(asctime)s %(message)s')

def get_price(instrument_key):
    if str(instrument_key).strip() == '':
        return None
    instrument_key = instrument_key
    df = pd.read_csv(DATA_FILE)
    instrument = df[df['instrument'] == instrument_key]
    if instrument.empty:
        return None
    else:
        return instrument.iloc[0]['ltp']
    

def get_open(instrument_key):
    if str(instrument_key).strip() == '':
        return None
    instrument_key = instrument_key
    df = pd.read_csv(DATA_FILE)
    instrument = df[df['instrument'] == instrument_key]
    if instrument.empty:
        return None
    else:
        return instrument.iloc[0]['open']
    
def get_high(instrument_key):
    if str(instrument_key).strip() == '':
        return None
    instrument_key = instrument_key
    df = pd.read_csv(DATA_FILE)
    instrument = df[df['instrument'] == instrument_key]
    if instrument.empty:
        return None
    else:
        return instrument.iloc[0]['high']
    
def get_low(instrument_key):
    if str(instrument_key).strip() == '':
        return None
    instrument_key = instrument_key
    df = pd.read_csv(DATA_FILE)
    instrument = df[df['instrument'] == instrument_key]
    if instrument.empty:
        return None
    else:
        return instrument.iloc[0]['low']

def get_close(instrument_key):
    if str(instrument_key).strip() == '':
        return None
    instrument_key = instrument_key
    df = pd.read_csv(DATA_FILE)
    instrument = df[df['instrument'] == instrument_key]
    if instrument.empty:
        return None
    else:
        return instrument.iloc[0]['close']

def get_segment(instrument_key):
    if str(instrument_key).strip() == '':
        return None
    instrument_key = instrument_key
    df = pd.read_csv(DATA_FILE)
    instrument = df[df['instrument'] == instrument_key]
    if instrument.empty:
        return None
    else:
        return instrument.iloc[0]['segment']

def get_market_data(instrument_key):
    if str(instrument_key).strip() == '':
        return None
    if get_price(instrument_key) in None:
        a = {instrument_key:
            {
                'symbol':'unknown',
                'segment':'unknown',
                'ltp':0,
                'high':0,
                'low':0,
                'open':0,
                'close':0,
            }
        }
        return a
    data = {instrument_key:
            {
                'symbol':get_symbol(instrument_key),
                'segment':get_segment(instrument_key),
                'ltp':float(get_price(instrument_key)),
                'high':float(get_high(instrument_key)),
                'low':float(get_low(instrument_key)),
                'open':float(get_open(instrument_key)),
                'close':float(get_close(instrument_key)),
            }
        }
    return data

# -=-=-=-=-=-=-=- NEW CODE -=-=-=-=-=-=-=-=
import upstox_client

def get_market_data(upstox_symbol_list):
    # Fetch all Upstox objects (assumed to have access tokens)
    upstox_tokens = Upstox.objects.all()
    
    for up in upstox_tokens:
        access_token = up.access_token
        configuration = upstox_client.Configuration()
        configuration.access_token = access_token
        api_instance = upstox_client.MarketQuoteApi(upstox_client.ApiClient(configuration))
        api_version = 'v-2'
        
        try:
            api_response = api_instance.get_full_market_quote(upstox_symbol_list, api_version)
            return api_response.to_dict()
        except Exception as e:
            logging.error("Exception when calling MarketQuoteApi->get_full_market_quote with access token %s: %s" % (access_token, e))
            # Continue to the next token
    
    # If all tokens fail, log the issue
    error_message = "All access tokens failed."
    logging.error(error_message)
    print(error_message)
    return None
