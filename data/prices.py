import csv
import random
import time
import requests
import upstox_client

DATA_FILE = 'C:\\Users\\atulg\\Desktop\\stock\\data\\data.csv'
# access_token = 'eyJ0eXAiOiJKV1QiLCJrZXlfaWQiOiJza192MS4wIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiIyOEFaNDUiLCJqdGkiOiI2NWI3ZGYzM2Y4MTU2YTcyMTBiYmQ0YmYiLCJpc011bHRpQ2xpZW50IjpmYWxzZSwiaXNBY3RpdmUiOnRydWUsInNjb3BlIjpbImludGVyYWN0aXZlIiwiaGlzdG9yaWNhbCJdLCJpYXQiOjE3MDY1NDkwNDMsImlzcyI6InVkYXBpLWdhdGV3YXktc2VydmljZSIsImV4cCI6MTcwNjU2NTYwMH0.gKvHwIsySuAneMqIdX6x4NsT32AsiPD_p3LS8LK6n6w'

def get_market_data(access_token, upstox_symbol_list):
    configuration = upstox_client.Configuration()
    configuration.access_token = access_token
    api_instance = upstox_client.MarketQuoteApi(upstox_client.ApiClient(configuration))
    api_version = 'v-2'

    try:
        api_response = api_instance.get_market_quote_ohlc(upstox_symbol_list, '1d',api_version)
        return api_response.to_dict()
    except Exception as e:
        print("Exception when calling MarketQuoteApi->get_full_market_quote: %s\n" % e)
        return None

def get_list():
    instruments = []
    # Open the CSV file and read the instruments
    with open(DATA_FILE, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            instrument = row['instrument']
            instruments.append(instrument)
    lst = ','.join(instruments)
    return lst

def update_csv_with_market_data(access_token):
    instruments = get_list()
    market_data = get_market_data(access_token,instruments)
    print(market_data)
    # Update CSV with market data
    with open(DATA_FILE, 'w', newline='') as csvfile:
        fieldnames = ['instrument', 'segment', 'ltp', 'open', 'close', 'low', 'high']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for instrument, data in market_data['data'].items():
            writer.writerow({
                'instrument': data['instrument_token'],
                'segment': instrument.split(':')[0],
                'ltp': data['last_price'],
                'open': data['ohlc']['open'],
                'close': data['ohlc']['close'],
                'low': data['ohlc']['low'],
                'high': data['ohlc']['high']
            })


while True:
    url = 'http://127.0.0.1:8000/upstox_access_tokens'
    response = requests.post(url=url)
    data = response.json()
    print('poora bahar')
    for x in data['tokens']:
        start_time = time.time()
        end_time = start_time + 10
        while time.time() < end_time:
            try:
                update_csv_with_market_data(x)
            except:
                break
            time.sleep(2)
        time.sleep(2)
      
