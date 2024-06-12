import pandas as pd
import random
import time

def price():
    a = random.randint(1,10)
    return a

# for i in range(0,100):
#     data_format = {
#         "instrument":['SBIN','RELIANCE','AXIS','KOTAK'],
#         "exchange":['NSE','NSE','NSE','NSE'],
#         "ltp":[price(),price(),price(),price()],
#         "open":[price(),price(),price(),price()],
#         "close":[price(),price(),price(),price()],
#         "low":[price(),price(),price(),price()],
#         "high":[price(),price(),price(),price()]
#     }
#     a =  pd.DataFrame(data_format)
#     a.to_csv('data.csv',index=False)
#     time.sleep(1)

data_format = {
        "instrument":['SBIN','RELIANCE','AXIS','KOTAK'],
        "exchange":['NSE','NSE','NSE','NSE'],
        "ltp":[price(),price(),price(),price()],
        "open":[price(),price(),price(),price()],
        "close":[price(),price(),price(),price()],
        "low":[price(),price(),price(),price()],
        "high":[price(),price(),price(),price()]
    }
a =  pd.DataFrame(data_format)
a.to_csv('data.csv',index=False)
print(a['instrument'])
print(a[a['instrument'] == 'SBIN'])
print(a[a['instrument'] == 'SBIN'].iloc[0]['ltp'])