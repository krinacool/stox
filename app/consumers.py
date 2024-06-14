import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from app.watchlist.price_stream import update_data
from stock.settings import SYMBOLS_FILE
import csv
from .models import symbols
import time

from channels.generic.websocket import WebsocketConsumer
import json

class StockConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        instruments = json.loads(text_data)
        response_data = []
        while True:
            for instrument in instruments:
                try:
                    # Assuming 'instrument' is something like 'NSE_EQ|INE062A01020'
                    # Fetch data from database based on symbol and segment
                    symbol_data = symbols.objects.get(instrument_key=instrument)
                    # Prepare data to send back to the client
                    response_data.append({
                        'instrument': instrument,
                        'data': {
                            'instrument': symbol_data.instrument_key,
                            'symbol': symbol_data.symbol,
                            'segment': symbol_data.segment,
                            'ltp': symbol_data.ltp,
                            'open': symbol_data.open,
                            'close': symbol_data.close,
                            'high': symbol_data.high,
                            'low': symbol_data.low,
                        }
                    })
                except symbols.DoesNotExist:
                    response_data.append({
                        'instrument': instrument,
                        'data': 'Symbol data not found'  # Handle error case
                    })
            # Send the response data back to the client
            self.send(text_data=json.dumps(response_data))
            time.sleep(1)





def symbol_search(search_string):
    csv_file = SYMBOLS_FILE
    results = []
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if search_string.lower() in row['tradingsymbol'].lower():
                if row['tradingsymbol'] == '':
                    continue
                results.append({'tradingsymbol': row['tradingsymbol'],'exchange_token': row['exchange_token'],'segment': row['exchange'], 'strike': row['strike'], 'expiry': row['expiry']})
            elif search_string.lower() in row['strike'].lower():
                if row['tradingsymbol'] == '':
                    continue
                results.append({'tradingsymbol': row['tradingsymbol'],'exchange_token': row['exchange_token'],'segment': row['exchange'], 'strike': row['strike'], 'expiry': row['expiry']})
            elif search_string.lower() in row['expiry'].lower():
                if row['tradingsymbol'] == '':
                    continue
                results.append({'tradingsymbol': row['tradingsymbol'],'exchange_token': row['exchange_token'],'segment': row['exchange'], 'strike': row['strike'], 'expiry': row['expiry']})
    return results[:40]

class PriceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.send_price_task = None

    async def disconnect(self, close_code):
        if self.send_price_task is not None:
            self.send_price_task.cancel()

        await self.close()

    async def receive(self, text_data):
        text_data = json.loads(text_data)
        symbol_list = text_data.get('symbol_list')
        data = update_data(eval(symbol_list))
        await self.send(text_data=json.dumps(data))
        self.send_price_task = asyncio.create_task(self.send_price_updates(symbol_list))

    async def send_price_updates(self,symbol_list):
        symbol_list = eval(symbol_list)
        while True:
            data = update_data(symbol_list)
            await self.send(text_data=json.dumps(data))
            await asyncio.sleep(1)


class SymbolList(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        await self.close()

    async def receive(self, text_data):
        await self.send(text_data)

        # Start sending updates every second after receiving a message
        self.send_price_task = asyncio.create_task(self.get_symbol_searched(text_data))

    async def get_symbol_searched(self,text_data):
        data = symbol_search(text_data)  # Replace with the logic to get the updated price
        await self.send(text_data=json.dumps(data))
        await asyncio.sleep(1)  # Wait for 1 second before sending the next update


def search(search_term):
    search_term = search_term.strip()
    if search_term[-1].isdigit():
        return search_op(search_term)
    matching_symbols = {key: value for key, value in symbollist.items() if search_term in key}
    # Get only the top 30 matching key-value pairs
    top_30_matches = dict(list(matching_symbols.items())[:30])
    return top_30_matches


# def search(search_term):
#     search_term = search_term.strip()
#     search_length = len(search_term)
#     start_term = search_term[:search_length // 3]
#     center_term = search_term[search_length // 3: 2 * (search_length // 3)]
#     end_term = search_term[2 * (search_length // 3):]
#     start_matches = {key: value for key, value in symbollist.items() if key.startswith(start_term)}
#     center_matches = {key: value for key, value in symbollist.items() if center_term in key and not key.startswith(center_term) and not key.endswith(center_term)}
#     end_matches = {key: value for key, value in symbollist.items() if key.endswith(end_term)}
#     all_matches = {**end_matches, **center_matches, **start_matches}
#     top_30_matches = dict(list(all_matches.items())[:30])
#     return top_30_matches



def search_op(search_term):
    search_length = len(search_term)
    part_length = search_length // 2
    start_term = search_term[:part_length]
    end_term = search_term[part_length:]
    start_matches = {key: value for key, value in symbollist.items() if key.startswith(start_term)}
    end_matches = {key: value for key, value in symbollist.items() if key.endswith(end_term)}
    all_matches = {**end_matches, **start_matches}
    top_30_matches = dict(list(all_matches.items())[:35])
    return top_30_matches



# def search(search_term):
#     search_term = search_term.strip()
#     search_length = len(search_term)
#     start_term = search_term[:search_length // 3]
#     center_term = search_term[search_length // 3: 2 * (search_length // 3)]
#     end_term = search_term[2 * (search_length // 3):]

#     def ignore_suffix(symbol):
#         # Ignore 'CE' or 'PE' suffixes
#         if symbol.endswith('CE'):
#             return symbol[:-2]
#         elif symbol.endswith('PE'):
#             return symbol[:-2]
#         return symbol

#     start_matches = {
#         key: value for key, value in symbollist.items()
#         if ignore_suffix(key).startswith(start_term)
#     }
#     center_matches = {
#         key: value for key, value in symbollist.items()
#         if center_term in ignore_suffix(key) and not ignore_suffix(key).startswith(center_term) and not ignore_suffix(key).endswith(center_term)
#     }
#     end_matches = {
#         key: value for key, value in symbollist.items()
#         if ignore_suffix(key).endswith(end_term)
#     }

#     all_matches = {**start_matches, **center_matches, **end_matches}
#     top_30_matches = dict(list(all_matches.items())[:30])
#     return top_30_matches





