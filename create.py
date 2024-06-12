import requests
import csv
import pyotp
import time


def create_csv():
    url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
    response = requests.get(url)
    if response.status_code == 200:
        print(200)
        data = response.json()
        csv_filename = "syb.csv"
        header = data[0].keys()
        with open(csv_filename, 'w', newline='') as csv_file:
            print('yo')
            csv_writer = csv.DictWriter(csv_file, fieldnames=header)
            csv_writer.writeheader()
            csv_writer.writerows(data)
        print(f"CSV file '{csv_filename}' has been created successfully.")
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")




create_csv()

time.sleep(2)
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


time.sleep(1)



import requests
import csv

def save_csv_from_url(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"CSV file saved as {filename}")
    else:
        print("Failed to download CSV file")

url = "https://images.dhan.co/api-data/api-scrip-master.csv"
filename = "dhan_syb.csv"


save_csv_from_url(url, filename)