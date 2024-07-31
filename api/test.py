# import requests

# # Define the endpoint and user credentials
# url = "http://127.0.0.1:8000/api/token/"
# credentials = {
#     "email": "admin@gmail.com",
#     "password": "password"
# }

# # Send the POST request to get the JWT token
# response = requests.post(url, data=credentials)

# if response.status_code == 200:
#     tokens = response.json()
#     access_token = tokens['access']
#     refresh_token = tokens['refresh']
#     print("Access Token:", access_token)
#     print("Refresh Token:", refresh_token)
# else:
#     print("Failed to get token:", response.status_code)
#     print(response.json())


# import requests

# # Define the place_order endpoint
# place_order_url = "http://127.0.0.1:8000/api/place_order/"

# # Order details
# order_data = {
#     "instrument": "NSE_EQ|INE062A01020",
#     "price": "123.45",
#     "quantity": 10,
#     "order_type": "BUY",
#     "product_type": "Intraday",
#     "type": "Market",
#     "stoploss": "100",
#     "target": "150"
# }

# # Headers including the JWT token for authorization
# headers = {
#     "Authorization": f"Bearer {access_token}",
#     "Content-Type": "application/json"
# }

# # Send the POST request to place an order
# response = requests.post(place_order_url, json=order_data, headers=headers)

# if response.status_code == 200:
#     print("Order placed successfully:", response.json())
# else:
#     print("Failed to place order:", response.status_code)
#     print(response.json())


# -=-=-==--=-=-=-=-=-=-=-=-=-=-GET POSITIONS -=-=-=-=-=-=-=-=-=-=-=-=-=-

import requests

# Base URL of your API
BASE_URL = "http://127.0.0.1:8000/api"

# Credentials for login
login_data = {
    "email": "admin@gmail.com",
    "password": "password"
}

# Function to obtain the JWT token
def get_jwt_token(base_url, login_data):
    response = requests.post(f"{base_url}/token/", data=login_data)
    if response.status_code == 200:
        return response.json()['access']
    else:
        raise Exception("Failed to obtain token")

# Function to fetch positions
def fetch_positions(base_url, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(f"{base_url}/positions/", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch positions: {response.status_code}")

def main():
    try:
        # Obtain JWT token
        token = get_jwt_token(BASE_URL, login_data)
        
        # Fetch positions
        positions = fetch_positions(BASE_URL, token)
        
        # Print positions
        for position in positions:
            print(position)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
