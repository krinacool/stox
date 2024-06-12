import websocket
import struct

# Define the WebSocket endpoint
ws_endpoint = "wss://api-feed.dhan.co"

# Function to send authorization and subscription packets
def send_auth_and_subscribe(client_id, access_token, instruments):
    # Header message structure for authorization packet
    auth_header = struct.pack("=bH30s50s", 11, 500, b"ClientID", b"DhanAuth")
    # Authorization packet structure
    auth_packet = struct.pack("=83s500s2s", auth_header, access_token.encode(), b"2P")
    # Send the authorization packet
    ws.send(auth_packet)

    # Prepare subscription packet
    num_instruments = len(instruments)
    subscription_header = struct.pack("=bH30s", 11, 2100, b"ClientID")
    # Convert instrument IDs to binary format
    instrument_data = b""
    for segment, security_id in instruments:
        instrument_data += struct.pack("=i20s", segment, str(security_id).encode())
    subscription_data = struct.pack("=i", num_instruments) + instrument_data
    subscription_packet = subscription_header + subscription_data
    # Send the subscription packet
    ws.send(subscription_packet)

# WebSocket event handlers
def on_open(ws):
    print("WebSocket connection established.")
    # Send authorization packet and subscribe to instruments when connection is opened
    send_auth_and_subscribe(client_id="1100617939", access_token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzEwOTQ0MzI4LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMDYxNzkzOSJ9.EgOe7NtglQKtUgU4s1zK83Gz8MWaezxav39lOaQXGEsz5RXIw2HILXRxbhL5hgOO6w_3xhNogvw7tUGHIDP99Q", instruments=[(5, "426247")])

def on_message(ws, message):
    print("Received message:", message)

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, close_status_code, close_msg):
    print(f"WebSocket connection closed with status code {close_status_code}: {close_msg}.")

if __name__ == "__main__":
    # Create WebSocket connection
    ws = websocket.WebSocketApp(ws_endpoint, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
    # Run the WebSocket
    ws.run_forever()
