import time
import random
from datetime import datetime

# Predefined lists for sensors and MAC addresses
sensors = ['sensor0', 'sensor1', 'sensor2','sensor3', 'sensor4', 'sensor5']
mac_addresses = ['40:B1:7F:BF:2E:2F', '54:B1:7F:BF:2E:3F', '68:B1:7F:BF:2E:4F']

# File path
file_path = 'sensor_data.txt'

while True:
    # Choose a random sensor, MAC address, and RSSI value
    sensor = random.choice(sensors)
    mac_address = random.choice(mac_addresses)
    rssi = random.randint(-180, 0)

    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    # Format the data string
    data = f"{sensor},{mac_address},{rssi},{timestamp}"

    try:
        # Write the data to the file
        with open(file_path, 'a') as file:
            file.write(data + '\n')
    except PermissionError:
         time.sleep(10)

    # Wait before writing the next line
    time.sleep(0.001)