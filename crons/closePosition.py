import requests
from datetime import datetime

current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Write the current time to a time.txt file
with open('time.txt', 'w') as file:
    file.write(f"Request made at: {current_time}")


# Make the request
response = requests.get('https://onstock.in/close_position')
print(response)

with open('res.txt', 'w') as file:
    file.write(f"Request made at: {response.content}")
