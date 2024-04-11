from device_locator import *
from datetime import datetime, timedelta
import time
import os
import json
import portalocker
from nref_floor2_graph import NREFFloor2Graph
from sensor import Sensor

# SENSOR POSITIONS: Coordinates of each sensor
all_sensors = {}
with open('sensorpositions.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        sensor_array = line.strip().split(",")
        all_sensors[sensor_array[0]] = Sensor((float(sensor_array[1]), float(sensor_array[2])))
    
# SENSOR GROUPS
sensor_groups = {
    tuple(['sensor_0','sensor_1','sensor_2']):['2-118','2-117'],
    tuple(['sensor_2','sensor_3','sensor_4']):['2-125'],
    tuple(['sensor_3','sensor_4','sensor_5']):['2-127','2-132','AST-8','ELV-179','2-002ZZ','STR-1'],
    tuple(['sensor_4','sensor_5','sensor_13']):['AST-2-132','2-002','2-011'],
    tuple(['sensor_14','sensor_13','sensor_15']):['STR-6','2-005ZZB','ELV-18X'],
    tuple(['sensor_15','sensor_14','sensor_23']):['2-090','2-005ZZA','2-060C','2-060B'],
    tuple(['sensor_23','sensor_0','sensor_22']):['STR-5','2-060A'],
    tuple(['sensor_23','sensor_21','sensor_22']):['2-052'],
    tuple(['sensor_21','sensor_20','sensor_19']):['2-043','2-050','STR-4'],
    tuple(['sensor_20','sensor_19','sensor_18']):['2-048','2-047','2-042'],
    tuple(['sensor_16','sensor_17','sensor_18']):['2-039','2-038','2-037'],
    tuple(['sensor_16','sensor_17','sensor_15']):['2-054'],
    tuple(['sensor_13','sensor_5','sensor_12']):['STR-2'],
    tuple(['sensor_6','sensor_7','sensor_8']):['Pedway','2-001ZZA','2-001','2-001ZZB','2-001ZZC','2-003'],
    tuple(['sensor_8','sensor_12','sensor_9']):['2-001ZZD'],
    tuple(['sensor_10','sensor_12','sensor_9']):['2-010','2-016'],
    tuple(['sensor_9','sensor_10','sensor_11']):['2-020','STR-3']
}

sensor_data = {}
eof_flag = 0
hour_counter = timedelta(seconds=0).total_seconds()  # Used for clearing BLEBeR data after an hour
hourly_timestamp = ""
is_first_line = True

class DataProcessing:
    '''
        Class that processes RSSI data for each sensor group
    '''
    def __init__(self, sensor_group, nodes):
        self.sensorA = all_sensors[sensor_group[0]]
        self.sensorB = all_sensors[sensor_group[1]]
        self.sensorC = all_sensors[sensor_group[2]]
        self.sensor_positions = [self.sensorA.coordinates, self.sensorB.coordinates, self.sensorC.coordinates]
        self.graph = NREFFloor2Graph
        self.node_coordinates = {}
        for node in nodes:
            self.node_coordinates[node] = self.graph.vertices[node].coordinates # graph vertices being monitored by the sensor group

        self.common_devices_keys = self.sensorA.devices.keys() & self.sensorB.devices.keys() & self.sensorC.devices.keys()
        # print(f"Common devices: {self.common_devices_keys}")
        self.common_devices_position = {}
        self.calculate_positions()
        self.process_heat()

    # Calculate the device position using trileration
    def calculate_positions(self):
        for common_device in self.common_devices_keys:
            # print(f"Calculating for {common_device}")

            rssi_A = self.sensorA.devices[common_device]
            distance_A = getSensorDistance(rssi_A)
            # print(f"distanceA:{distance_A}")

            rssi_B = self.sensorB.devices[common_device]
            distance_B = getSensorDistance(rssi_B)
            # print(f"distanceB:{distance_B}")

            rssi_C = self.sensorC.devices[common_device]
            distance_C = getSensorDistance(rssi_C)
            # print(f"distanceC:{distance_C}")

            distances = [distance_A, distance_B, distance_C]

            # print(f"Sensor Positions: {self.sensor_positions}")
            device_position = trilaterate(self.sensor_positions, distances)
            self.common_devices_position[common_device] = device_position
    
    def process_heat(self):
        for device, position in self.common_devices_position.items():
            correct_node = determine_node(position, self.node_coordinates)
            # print("correct node:" + correct_node)
            self.graph.vertices[correct_node].increase_heat()


def get_data_from_txt() -> int:
    global sensor_data, hour_counter, eof_flag, hourly_timestamp, is_first_line
    prev_date_obj = datetime.now()
    total_time = timedelta(seconds=0).total_seconds()
    eof_flag = 0 # if there no more lines in sensor_data.txt, it will try 10 times before it quits

    # hundred_milliseconds = timedelta(milliseconds=100)

    with open('sensor_data.txt', 'r') as file:
        if os.path.getsize('sensor_data.txt') == 0:
            time.sleep(100)
        while True:
            line = file.readline()
            print(line)
            if not line:
                # No new line is available, wait before trying to read again
                eof_flag += 1 # start counting
                if eof_flag == 10:
                    return
                continue

            line_array = line.strip().split(",")
            try:
                # print(f"line array: {line_array}")
                sensor_id = line_array[0].strip()
                device_addr = line_array[1].strip()
                rssi = line_array[2].strip()
                date_str = line_array[3].strip()
            except IndexError:
                continue

            eof_flag = 0 # there are still lines
            # Convert the string to a datetime object
            date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")

            if is_first_line == True:
                prev_date_obj = date_obj
                hourly_timestamp = date_obj.strftime("%Y-%m-%d %H:%M:%S.%f") # What hour is this processing for?
                print("----------------------------------------------------------------------"+hourly_timestamp)
                is_first_line = False
                continue

            # Only collect data within 3 second interval
            delta = date_obj - prev_date_obj
            prev_date_obj = date_obj

            total_time += delta.total_seconds()
            if total_time >= 5:
                # print(total_time)
                hour_counter += total_time
                return
            try:
                sensor_data[sensor_id][device_addr].append(int(rssi))
            except KeyError: # Initialize value
                if sensor_id not in sensor_data.keys():
                    sensor_data[sensor_id]= {}
                if device_addr not in sensor_data[sensor_id].keys():
                    sensor_data[sensor_id][device_addr] = []
                sensor_data[sensor_id][device_addr].append(int(rssi))

def clear_data():
    global hour_counter
    hour_counter = timedelta(seconds=0).total_seconds()

    with open('sensor_data.txt', 'a') as file:
        portalocker.lock(file, portalocker.LOCK_EX)

        # Truncate the file to zero length
        with open('sensor_data.txt', 'w'):
            pass

def reset_heat():
    for vertex_id, vertex_class in NREFFloor2Graph.vertices.items():
        vertex_class.heat_level = 0

def get_json_file():
    with open('heat_data.json', 'r') as file:
        heat_data = json.load(file)
    return heat_data

def update_heat_json(data) -> None:
    with open('heat_data.json', 'w') as file:
        json.dump(data, file, indent=4)
    
def save_heat(timestamp):
    heat_levels = {}
    for vertex_id, vertex_class in NREFFloor2Graph.vertices.items():
        heat_levels[vertex_id] = vertex_class.heat_level

    # Determine the exact hour where the heat data must be saved
    date = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
    month = str(date.month)
    day = str(date.weekday())
    hour = f"{date.hour}00"

    heat_json = get_json_file()
    heat_json[month][day][hour] = {"heat": heat_levels}

    update_heat_json(heat_json)


def main():
    global sensor_data, eof_flag, hour_counter, hourly_timestamp

    while True: # Heat_levels are updated every 5 seconds
        # If it is one hour, save final heat level for the hour  
        if hour_counter >= 3600 or eof_flag >= 10: # Change to 3600 for one hour
            print("////////////////////////////////////////////////////"+hourly_timestamp)
            save_heat(hourly_timestamp)
            reset_heat()

            clear_data()
            for sensor in sensor_data.keys():
                all_sensors[sensor].clear_devices()
                
        get_data_from_txt()
        print(hourly_timestamp)

        for sensor, device in sensor_data.items():
            for device_id, rssi_array in device.items():
                all_sensors[sensor].add_device(device_id, rssi_array)

        '''
        STEP 2: Process data per sensor group
        # DataProcessing class gather RSSI data, convert them to distances, pinpoint the exact vertex where the device is located, 
            and increase the heat of vertices
        # Since we are only working with three sensors, we will only process one sensor group
        # TODO: There should be a for loop to process data for all sensor groups in sensor_groups dictionary
        '''
        data_processing = DataProcessing(['sensor_0', 'sensor_1', 'sensor_2'], sensor_groups[('sensor_0', 'sensor_1', 'sensor_2')])
        data_processing = DataProcessing(['sensor_2', 'sensor_3', 'sensor_4'], sensor_groups[('sensor_2', 'sensor_3', 'sensor_4')])
        data_processing = DataProcessing(['sensor_3', 'sensor_4', 'sensor_5'], sensor_groups[('sensor_3', 'sensor_4', 'sensor_5')])
        data_processing = DataProcessing(['sensor_4', 'sensor_5', 'sensor_13'], sensor_groups[('sensor_4', 'sensor_5', 'sensor_13')])
        data_processing = DataProcessing(['sensor_14', 'sensor_13', 'sensor_15'], sensor_groups[('sensor_14', 'sensor_13', 'sensor_15')])
        data_processing = DataProcessing(['sensor_15', 'sensor_14', 'sensor_23'], sensor_groups[('sensor_15', 'sensor_14', 'sensor_23')])
        data_processing = DataProcessing(['sensor_23', 'sensor_0', 'sensor_22'], sensor_groups[('sensor_23', 'sensor_0', 'sensor_22')])
        data_processing = DataProcessing(['sensor_23', 'sensor_21', 'sensor_22'], sensor_groups[('sensor_23', 'sensor_21', 'sensor_22')])
        data_processing = DataProcessing(['sensor_21', 'sensor_20', 'sensor_19'], sensor_groups[('sensor_21', 'sensor_20', 'sensor_19')])
        data_processing = DataProcessing(['sensor_20', 'sensor_19', 'sensor_18'], sensor_groups[('sensor_20', 'sensor_19', 'sensor_18')])
        data_processing = DataProcessing(['sensor_16', 'sensor_17', 'sensor_18'], sensor_groups[('sensor_16', 'sensor_17', 'sensor_18')])
        data_processing = DataProcessing(['sensor_16', 'sensor_17', 'sensor_15'], sensor_groups[('sensor_16', 'sensor_17', 'sensor_15')])
        data_processing = DataProcessing(['sensor_13', 'sensor_5', 'sensor_12'], sensor_groups[('sensor_13', 'sensor_5', 'sensor_12')])
        data_processing = DataProcessing(['sensor_6', 'sensor_7', 'sensor_8'], sensor_groups[('sensor_6', 'sensor_7', 'sensor_8')])
        data_processing = DataProcessing(['sensor_8', 'sensor_12', 'sensor_9'], sensor_groups[('sensor_8', 'sensor_12', 'sensor_9')])
        data_processing = DataProcessing(['sensor_10', 'sensor_12', 'sensor_9'], sensor_groups[('sensor_10', 'sensor_12', 'sensor_9')])
        data_processing = DataProcessing(['sensor_9', 'sensor_10', 'sensor_11'], sensor_groups[('sensor_9', 'sensor_10', 'sensor_11')])
        

if __name__ == "__main__":
    main()