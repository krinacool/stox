import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db import models
from asgiref.sync import sync_to_async  # Import sync_to_async for Django <= 4.0
# from django.db import sync_to_async  # Use this for Django >= 4.1

class StockConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        from .models import symbols
        instruments = json.loads(text_data)
        
        try:
            while True:
                response_data = []
                for instrument in instruments:
                    try:
                        symbol_data = await self.get_symbol_data(instrument)
                        syb = symbol_data.symbol
                        if syb.strip() == "":
                            syb = symbols.instrument_key
                        response_data.append({
                            'instrument': instrument,
                            'data': {
                                'instrument': symbol_data.instrument_key,
                                'symbol': syb,
                                'name': symbol_data.name,
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
                            'data': 'Symbol data not found'
                        })
                
                # Send the response data back to the client
                await self.send(text_data=json.dumps(response_data))
                
                # Use a small delay to avoid high CPU usage in tight loops
                await asyncio.sleep(2)
        
        except Exception as e:
            # Log the exception for debugging
            print(f"Exception in WebSocket receive loop: {e}")
            # You may want to close the connection or handle this error case

    @sync_to_async
    def get_symbol_data(self, instrument):
        from .models import symbols
        return symbols.objects.get(instrument_key=instrument)
