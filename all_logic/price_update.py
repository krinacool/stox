from smartapi import SmartConnect
import pyotp
import time

api_key = 'qy5tDMrp'
clientId = 'A400396'
pwd = '0786'
smartApi = SmartConnect(api_key)
token = "HPT2ZFLWDZMD77EAGVIEDQTQMI"
totp=pyotp.TOTP(token).now()
print(totp)
correlation_id = "abc123"
# login api call
data = smartApi.generateSession(clientId, pwd, totp)
print(data)
print("----------")
if data == "{'success': False, 'message': 'Invalid Token', 'errorCode': 'AG8001', 'data': ''}":
    print("hello")

print(smartApi)
i = 0
# print(smartApi.orderBook())
while True:
    get = smartApi.ltpData('NFO','BANKNIFTY11OCT2344400CE','40100')
    print(get)
    print(get['data']['ltp'])
    print(i)
    i+=1
    time.sleep(1)

