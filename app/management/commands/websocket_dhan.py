from django.core.management.base import BaseCommand
from dhanhq import marketfeed
from django.db.models import Q
from asgiref.sync import sync_to_async
from app.models import Watchlist
import threading


# Define your DHAN API credentials
client_id = "1100617939"
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzEwOTQ0MzI4LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMDYxNzkzOSJ9.EgOe7NtglQKtUgU4s1zK83Gz8MWaezxav39lOaQXGEsz5RXIw2HILXRxbhL5hgOO6w_3xhNogvw7tUGHIDP99Q"

# Define the instruments to subscribe to
instruments = [(5, "426247")]

# Define the subscription code
subscription_code = marketfeed.Quote

print(subscription_code)

# Define the callback functions for connection and receiving messages
async def on_connect(instance):
    print("Connected to WebSocket")


async def keep_connection_alive(ws):
    try:
        while True:
            # Wait for Ping from server
            ping_msg = await ws.recv()

            # Respond with Pong to maintain connection
            if ping_msg == b'Ping':
                print('Ping')
                await ws.send('Pong')
    except :
        # Connection closed by server, handle reconnection here
        print("Connection closed by server, reconnecting...")
        # Call your reconnect logic here
        # Example: await connect_to_websocket()


async def on_message(instance, message):
    instance.subscribe_symbols(1,[(5, "426247"),(1, "3045")])
    token = message['security_id']
    ob = await get_watchlist(token)
    print(message)
    if 'ping' in str(message).lower():
        print('Shi baat hai')
    try:
        ob.ltp = message['LTP']
        await save_watchlist(ob)
    except:
        pass





@sync_to_async
def get_watchlist(token):
    return Watchlist.objects.filter(token=token).first()

@sync_to_async
def save_watchlist(ob):
    ob.save()

# Create a Django management command class
class Command(BaseCommand):
    help = 'Connect to DHAN API WebSocket and retrieve real-time market data'

    def handle(self, *args, **kwargs):
        print(f"Subscription code: {subscription_code}")

        # Initialize DHAN API WebSocket feed
        feed = marketfeed.DhanFeed(client_id,
                                   access_token,
                                   instruments,
                                   subscription_code,
                                   on_connect=on_connect,
                                   on_message=on_message)

        # Start the WebSocket feed
        feed.run_forever()
        print('RUN AGAIN')
        import os
        os.system('python manage.py websocket_dhan')