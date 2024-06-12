import hashlib
import requests
import json
from app.symbols.getsymbols import exc_symbols
from settings.models import *

symbollist = {}
symboldata = exc_symbols()
for i in symboldata:
    temp = {'symbol':i,'segment':symboldata[i]['exchange'],'token':symboldata[i]['token']}
    symbollist[i] = temp

def checksum(input_string):
    sha256 = hashlib.sha256()
    sha256.update(input_string.encode('utf-8'))
    checksum = sha256.hexdigest()
    return checksum


def alice_order(symbol,quantity,order_type,product):
    try:
        print("alice_order")
        segment = symbollist[symbol]['segment']
        token = symbollist[symbol]['token']
        api = Api.objects.first()
        userid = api.user_id
        apikey = api.api_key
        url = 'https://ant.aliceblueonline.com/rest/AliceBlueAPIService/api/customer/getAPIEncpkey'
        payload = json.dumps({
          "userId": userid,
          "userData": apikey
        })
        headers = {
          'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        a = response.json()
        enckey = a['encKey']
        # SESSION ID
        url = 'https://ant.aliceblueonline.com/rest/AliceBlueAPIService/api/customer/getUserSID'
        ch = checksum(f"{userid}{apikey}{enckey}")
        payload = json.dumps({
          "userId": userid,
          "userData": ch
        })
        headers = {
          'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        sessionID = response.json()['sessionID']
        # PLACE ORDER
        url = 'https://ant.aliceblueonline.com/rest/AliceBlueAPIService/api/placeOrder/executePlaceOrder'
        payload = json.dumps([
          {
            "complexty": "regular",
            "discqty": "0",
            "exch": segment,
            "pCode": "MIS",
            "prctyp": "MKT",
            "price": "0.0",
            "qty": quantity,
            "ret": "DAY",
            "symbol_id": token,
            "trading_symbol": symbol,
            "transtype": order_type,
            "trigPrice": "",
            "orderTag": "onstock"
          }
        ])
        headers = {
          'Authorization': f'Bearer {userid} {sessionID}',
          'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        nordno = response.json()
        print(nordno)
    except Exception as e:
        print(e)
    