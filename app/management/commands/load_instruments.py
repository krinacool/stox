import csv
from django.core.management.base import BaseCommand
from django.db import transaction
from app.models import Instrument, Watchlist, symbols, Shoonya_Instrument  # Corrected model name to 'Symbol'
import requests
import gzip
import shutil
import zipfile
import os
import pandas as pd


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


def combine_txt_to_csv(input_folder, output_file):
    # Define all possible columns
    all_columns = [
        "Exchange", "Token", "LotSize", "Symbol", "TradingSymbol", 
        "Expiry", "Instrument", "OptionType", "StrikePrice", "TickSize", 
        "Precision", "Multiplier", "GNGD"
    ]
    
    # List to hold DataFrames
    df_list = []

    # Iterate over all txt files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            filepath = os.path.join(input_folder, filename)
            # Read the file into a DataFrame
            df = pd.read_csv(filepath)
            # Add missing columns with NaN values
            for column in all_columns:
                if column not in df.columns:
                    df[column] = pd.NA
            # Reorder columns to match the order of all_columns
            df = df[all_columns]
            # Append DataFrame to the list
            df_list.append(df)

    # Concatenate all DataFrames
    combined_df = pd.concat(df_list, ignore_index=True)
    # Save the combined DataFrame to a CSV file
    combined_df.to_csv(output_file, index=False)

    print(f"Combined CSV saved to {output_file}")

def download_and_extract(urls, target_folder):
    for url in urls:
        # Extract filename from URL
        filename = url.split('/')[-1]
        
        # Download the file
        response = requests.get(url)
        if response.status_code == 200:
            # Save the downloaded ZIP file
            zip_file_path = os.path.join(target_folder, filename)
            with open(zip_file_path, 'wb') as f:
                f.write(response.content)
                
            # Extract the ZIP file
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(target_folder)
                
            # Remove the ZIP file after extraction
            os.remove(zip_file_path)
            
            print(f"Downloaded and extracted: {filename}")
        else:
            print(f"Failed to download: {filename}")

# Example usage
urls = [
    "https://api.shoonya.com/NSE_symbols.txt.zip",
    "https://api.shoonya.com/NFO_symbols.txt.zip",
    "https://api.shoonya.com/CDS_symbols.txt.zip",
    "https://api.shoonya.com/MCX_symbols.txt.zip",
    "https://api.shoonya.com/BSE_symbols.txt.zip",
    "https://api.shoonya.com/BFO_symbols.txt.zip",
    "https://api.shoonya.com/NCX_symbols.txt.zip"
]
target_folder = "./ShoonyaFiles"  # Set your target folder path here
# Create the target folder if it doesn't exist
os.makedirs(target_folder, exist_ok=True)

# Call the function to download and decompress the file
class Command(BaseCommand):
    help = 'Load instruments from CSV'

    def handle(self, *args, **kwargs):
        # URL of the .gz file
        url = "https://assets.upstox.com/market-quote/instruments/exchange/complete.csv.gz"
        # Output file name
        output_filename = "complete.csv"
        download_and_decompress(url, output_filename)
        download_and_extract(urls, target_folder)
        combine_txt_to_csv(target_folder, 'shoonya.csv')
        file_path = 'complete.csv'
        # Delete all existing instruments
        Shoonya_Instrument.objects.all().delete()
        shoonya = []
        with open('shoonya.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Check if last_price is not 0 before appending
                shoonya.append(Instrument(
                    exchange_token=row['Token'] if row['Token'] else None,
                    tradingsymbol=row['TradingSymbol'] if row['TradingSymbol'] else None,
                    name=row['Symbol'],
                    exchange=row['Exchange'],
                ))

        # Bulk create all shoonya in a single transaction
        with transaction.atomic():
            Shoonya_Instrument.objects.bulk_create(shoonya, batch_size=1000)

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
            else:
                x.last_day_close = x.close
                x.save()

        self.stdout.write(self.style.SUCCESS('Successfully loaded instruments'))
