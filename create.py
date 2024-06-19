import requests
import time
import requests
import gzip
import shutil

# URL of the .gz file
url = "https://assets.upstox.com/market-quote/instruments/exchange/complete.csv.gz"
# Output file name
output_filename = "complete.csv"

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
download_and_decompress(url, output_filename)