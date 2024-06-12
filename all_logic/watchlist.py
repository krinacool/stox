import csv

def update_symbols(instrument,exchange):
    # Read existing data from the CSV file
    instrument_data = [instrument, exchange, 0, 0, 0, 0, 0]
    csv_file_path = 'data.csv'
    existing_data = []
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        existing_data = list(reader)
    instrument_exists = any(row[0] == instrument_data[0] for row in existing_data)
    if not instrument_exists:
        with open(csv_file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(instrument_data)
        return True
    else:
        return False


print(update_symbols('OPPO2','NSE'))
