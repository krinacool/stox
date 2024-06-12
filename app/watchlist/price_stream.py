from threading import Thread
from app.symbols.details import get_price,get_market_data
import queue
import json

# def update_data(symbol_list):
#     # WATCHLIST
#     userwatchlist = []
#     watchlist = []
#     data = {}
#     for i in symbol_list:
#         temp = {"symbol":i}
#         watchlist.append(i)
#         userwatchlist.append(temp)
#     data.update({"symbollist":watchlist})
#     n_threads = len(userwatchlist)
#     thread_list = []
#     que = queue.Queue()
#     for i in range(n_threads):
#         thread = Thread(target=lambda q,arg1: q.put({userwatchlist[i]['symbol']:get_data(arg1)}), args = (que, userwatchlist[i]['symbol']))
#         thread_list.append(thread)
#         thread_list[i].start()

#     for thread in thread_list:
#         thread.join()

#     while not que.empty():
#         result = que.get()
#         data.update(result)
#     return data

# import concurrent.futures
# def update_data(symbol_list):
#     data = {"symbollist": symbol_list}
#     with concurrent.futures.ThreadPoolExecutor(max_workers=len(symbol_list)) as executor:
#         # Define a function to fetch data
#         def fetch_data(symbol):
#             return {symbol: get_data(symbol)}
#         # Submit tasks to the ThreadPoolExecutor
#         futures = {executor.submit(fetch_data, symbol): symbol for symbol in symbol_list}
#         for future in concurrent.futures.as_completed(futures):
#             symbol = futures[future]
#             try:
#                 result = future.result()
#                 data.update(result)
#             except Exception as e:
#                 pass
#     return data



def transform_data(symbols, input_data):
    output_data = {"data": {}}
    output_data['data']['symbollist'] = symbols

    for symbol in symbols:
        matching_key = next((key for key in input_data['data'] if symbol in key), None)
        
        if matching_key:
            symbol_data = input_data['data'][matching_key]
            ohlc_data = symbol_data.get('ohlc', {})

            temp = {
                "tradingsymbol": symbol,
                "symboltoken": symbol_data.get('instrument_token', ''),
                "open": ohlc_data.get('open', 0),
                "high": ohlc_data.get('high', 0),
                "low": ohlc_data.get('low', 0),
                "close": ohlc_data.get('close', 0),
                "ltp": symbol_data.get('last_price', 0)
            }

            output_data['data'][symbol] = temp
    return output_data


# def update_data2(symbol_list):
#     try:
#         temp_list = []
#         for x in symbol_list:
#             data = symbollist.get(x)
#             temp_list.append(get_instrument(data['token']))
#         upstox_symbol_list = ','.join(temp_list)
#         market_data = get_market_data(upstox_symbol_list)
#         market_data = transform_data(symbol_list,market_data)
#         return market_data
#     except Exception as e:
#         pass


def update_data(symbol_list):
    mdata = {}
    for x in symbol_list:
        mdata.update(get_market_data(x))
    return mdata

# import concurrent.futures

# def chunk_list(lst, chunk_size):
#     for i in range(0, len(lst), chunk_size):
#         yield lst[i:i + chunk_size]

# def update_data(symbol_list):
#     data = {"symbollist": symbol_list}
#     chunked_symbols = list(chunk_list(symbol_list, chunk_size=1000))  # Adjust batch size as needed

#     with concurrent.futures.ProcessPoolExecutor(max_workers=len(chunked_symbols)) as executor:
#         for symbols_chunk in chunked_symbols:
#             # Define a function to fetch data for a chunk of symbols
#             def fetch_data_for_chunk(symbol_chunk):
#                 return {symbol: get_data(symbol) for symbol in symbol_chunk}

#             # Submit tasks to the ProcessPoolExecutor for each chunk
#             futures = {executor.submit(fetch_data_for_chunk, symbols_chunk): symbols_chunk}

#             for future in concurrent.futures.as_completed(futures):
#                 symbols_chunk = futures[future]
#                 try:
#                     result = future.result()
#                     data.update(result)
#                 except Exception as e:

#     return data


