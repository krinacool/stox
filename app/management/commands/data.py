from django.core.management.base import BaseCommand
from django.db import transaction
from app.models import symbols
from app.symbols.details import get_market_data
import time
import logging

# Configure logging
logging.basicConfig(filename='update_symbols.log', level=logging.ERROR, format='%(asctime)s %(message)s')

class Command(BaseCommand):
    help = 'Update all symbols data in the db'

    def handle(self, *args, **kwargs):
        while True:
            instrument_keys = symbols.objects.values_list('instrument_key', flat=True).distinct()
            instrument_keys_list = list(instrument_keys)
            
            if not instrument_keys_list:
                self.stdout.write(self.style.WARNING('No instrument keys found in the database.'))
            else:
                instrument_keys_str = ','.join(instrument_keys_list)
                market_data = get_market_data(instrument_keys_str)
                
                if market_data:
                    symbols_to_update = []
                    for x in market_data.get('data', {}):
                        try:
                            instrument = market_data['data'][x]['instrument_token']
                            stock = symbols.objects.get(instrument_key=instrument)
                            stock.ltp = market_data['data'][x]['last_price']
                            stock.open = market_data['data'][x]['ohlc']['open']
                            stock.close = market_data['data'][x]['ohlc']['close']
                            stock.high = market_data['data'][x]['ohlc']['high']
                            stock.low = market_data['data'][x]['ohlc']['low']
                            symbols_to_update.append(stock)
                        except symbols.DoesNotExist:
                            logging.error(f"Symbol with instrument key {instrument} does not exist.")
                        except Exception as e:
                            logging.error(f"Error updating symbol with instrument key {instrument}: {e}")
                    
                    # Bulk update symbols
                    if symbols_to_update:
                        try:
                            with transaction.atomic():
                                symbols.objects.bulk_update(symbols_to_update, ['ltp', 'open', 'close', 'high', 'low'])
                        except Exception as e:
                            logging.error(f"Error during bulk update: {e}")
                else:
                    logging.error("Failed to fetch market data.")
                    
            time.sleep(0.5)
