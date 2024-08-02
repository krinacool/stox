import requests

# Define the endpoint and user credentials
url = "https://onstock.in/api/token/"
credentials = {
    "email": "admin@gmail.com",
    "password": "password"
}

# Send the POST request to get the JWT token
response = requests.post(url, data=credentials)

if response.status_code == 200:
    tokens = response.json()
    access_token = tokens['access']
    refresh_token = tokens['refresh']
    print("Access Token:", access_token)
    print("Refresh Token:", refresh_token)
else:
    print("Failed to get token:", response.status_code)
    print(response.json())


import requests

# Define the place_order endpoint
place_order_url = "https://onstock.in/api/place_order/"

# Order details
order_data = {
    "instrument": "NSE_EQ|INE062A01020",
    "price": "123.45",
    "quantity": 10,
    "order_type": "BUY",
    "product_type": "Intraday",
    "type": "Market",
    # "stoploss": "100",
    # "target": "150"
}

# Headers including the JWT token for authorization
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Send the POST request to place an order
response = requests.post(place_order_url, json=order_data, headers=headers)

if response.status_code == 200:
    print("Order placed successfully:", response.json())
else:
    print("Failed to place order:", response.status_code)
    print(response.json())
