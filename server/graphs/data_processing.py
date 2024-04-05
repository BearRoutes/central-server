from nref_floor2_graph import NREFFloor2Graph
from sensor import Sensor
from device_locator import *

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
            print(f"distanceA:{distance_A}")

            rssi_B = self.sensorB.devices[common_device]
            distance_B = getSensorDistance(rssi_B)
            print(f"distanceB:{distance_B}")

            rssi_C = self.sensorC.devices[common_device]
            distance_C = getSensorDistance(rssi_C)
            print(f"distanceC:{distance_C}")

            distances = [distance_A, distance_B, distance_C]

            print(f"Sensor Positions: {self.sensor_positions}")
            device_position = trilaterate(self.sensor_positions, distances)
            self.common_devices_position[common_device] = device_position
    
    def process_heat(self):
        for device, position in self.common_devices_position.items():
            correct_node = determine_node(position, self.node_coordinates)
            # print("correct node:" + correct_node)
            self.graph.vertices[correct_node].increase_heat()

