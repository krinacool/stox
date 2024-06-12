import pandas as pd

def get_price(instrument_key):
    if str(instrument_key).strip() == '':
        return None
    instrument_key = instrument_key
    df = pd.read_csv('data.csv')
    instrument = df[df['instrument'] == instrument_key]
    if instrument.empty:
        return None
    else:
        return instrument.iloc[0]['ltp']
    
