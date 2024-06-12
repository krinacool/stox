import csv

def get_symbol_name(token):
    csv_file = 'syb.csv'  # Path to your CSV file
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if int(row['token']) == token:
                return row['symbol']
    return None

# Example usage:
token = 10243  # Token for which you want to get symbol and name

print('')
print('')
print(get_symbol_name(3045))