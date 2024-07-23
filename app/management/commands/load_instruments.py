import csv
from django.core.management.base import BaseCommand
from django.db import transaction
from app.models import Instrument, Watchlist, symbols  # Corrected model name to 'Symbol'
import requests
import requests
import gzip
import shutil


def download_and_decompress(url, output_filename):
    # Download the .gz file
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        # Save the .gz file
        with open(output_filename + ".gz", 'wb') as f:
            f.write(response.content)
        
        # Decompress the .gz file
        with gzip.open(output_filename + ".gz", 'rb') as f_in:
            with open(output_filename, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        print("Download and decompression successful.")
    else:
        print("Failed to download the file.")

# Call the function to download and decompress the file

class Command(BaseCommand):
    help = 'Load instruments from CSV'

    def handle(self, *args, **kwargs):
        # URL of the .gz file
        url = "https://assets.upstox.com/market-quote/instruments/exchange/complete.csv.gz"
        # Output file name
        output_filename = "complete.csv"
        download_and_decompress(url, output_filename)
        file_path = 'complete.csv'
        # Delete all existing instruments
        Instrument.objects.all().delete()
        instruments = []
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Check if last_price is not 0 before appending
                last_price = float(row['last_price']) if row['last_price'] else None
                if last_price != 0 and last_price is not None:
                    instruments.append(Instrument(
                        instrument_key=row['instrument_key'],
                        exchange_token=row['exchange_token'] if row['exchange_token'] else None,
                        tradingsymbol=row['tradingsymbol'] if row['tradingsymbol'] else None,
                        name=row['name'],
                        last_price=last_price,
                        expiry=row['expiry'] if row['expiry'] else None,
                        strike=float(row['strike']) if row['strike'] else None,
                        tick_size=float(row['tick_size']) if row['tick_size'] else None,
                        lot_size=int(row['lot_size']) if row['lot_size'] else None,
                        instrument_type=row['instrument_type'],
                        option_type=row['option_type'] if row['option_type'] else None,
                        exchange=row['exchange'],
                    ))

        # Bulk create all instruments in a single transaction
        with transaction.atomic():
            Instrument.objects.bulk_create(instruments, batch_size=1000)
        
        # Update watchlist based on instruments
        watchlist = Watchlist.objects.all()
        for x in watchlist:
            if not Instrument.objects.filter(instrument_key=x.instrument_key).exists():
                x.delete()
        
        # Update symbols based on instruments
        symbol = symbols.objects.all()
        for x in symbol:
            if not Instrument.objects.filter(instrument_key=x.instrument_key).exists():
                x.delete()

        self.stdout.write(self.style.SUCCESS('Successfully loaded instruments'))
