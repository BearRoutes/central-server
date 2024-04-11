import time
import random
from datetime import datetime, timedelta

# Predefined lists for sensors and MAC addresses
sensors = ['sensor_0', 'sensor_1', 'sensor_2', 'sensor_3', 'sensor_4', 'sensor_5', 'sensor_6', 'sensor_7', 'sensor_8', 'sensor_9', 'sensor_10', 'sensor_11', 'sensor_12', 'sensor_13', 'sensor_14', 'sensor_15', 'sensor_16', 'sensor_17', 'sensor_18', 'sensor_19', 'sensor_20', 'sensor_21', 'sensor_22']
# sensors = ['sensor_22', 'sensor_23', 'sensor_0','sensor_6', 'sensor_7', 'sensor_8']
mac_addresses = ['40:B1:7F:BF:2E:2F', '54:B1:7F:BF:2E:3F']

# File path
file_path = 'sensor_data.txt'

date_str = '2024-04-10 8:30:00.000'

# Convert the string to a datetime object
timestamp = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f')
end_time = timestamp + timedelta(seconds=3600)

while True:
    # Choose a random sensor, MAC address, and RSSI value
    sensor = random.choice(sensors)
    mac_address = random.choice(mac_addresses)
    rssi = random.randint(-80, 0)

    # Get the current timestamp
    # timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    timestamp += timedelta(milliseconds=1)
    # timestamp = time.strptime("%Y-%m-%d %H:%M:%S.%f")
    if timestamp >= end_time:
        break

    timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")
    # Format the data string
    data = f"{sensor},{mac_address},{rssi},{timestamp_str}"

    try:
        # Write the data to the file
        with open(file_path, 'a') as file:
            file.write(data + '\n')
    except PermissionError:
         time.sleep(1)

    # Wait before writing the next line
    # time.sleep(0.01)