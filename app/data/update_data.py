from dhanhq import marketfeed

# Add your Dhan Client ID and Access Token
client_id = "1100617939"
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzEwOTQ0MzI4LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMDYxNzkzOSJ9.EgOe7NtglQKtUgU4s1zK83Gz8MWaezxav39lOaQXGEsz5RXIw2HILXRxbhL5hgOO6w_3xhNogvw7tUGHIDP99Q"

# Maximum 100 instruments can be subscribed, then use 'subscribe_symbols' function 

instruments = [(5, "426247")]

# Type of data subscription
subscription_code = marketfeed.Depth

# Ticker - Ticker Data
# Quote - Quote Data
# Depth - Market Depth


async def on_connect(instance):
    print("Connected to websocket")

async def on_message(instance, message):
    print(message)
    print()
    print()
    print('-=-=-=-=-=-=-=--=-')
    for x in message:
        print('================+++++++++++++++++++++=================')
        print(x)


print(f"Subscription code :{subscription_code}")

feed = marketfeed.DhanFeed(client_id,
    access_token,
    instruments,
    subscription_code,
    on_connect=on_connect,
    on_message=on_message)

feed.run_forever()
