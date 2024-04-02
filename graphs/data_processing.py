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
    tuple(['sensor0','sensor1','sensor2']):['2-118','2-117'],
    tuple(['sensor2','sensor3','sensor4']):['2-125'],
    tuple(['sensor3','sensor4','sensor5']):['2-127','2-132','AST-8','ELV-179','2-002ZZ','STR-1'],
    tuple(['sensor4','sensor5','sensor13']):['AST-2-132','2-002','2-011'],
    tuple(['sensor14','sensor13','sensor15']):['STR-6','2-005ZZB','ELV-18X'],
    tuple(['sensor15','sensor14','sensor23']):['2-090','2-005ZZA','2-060C','2-060B'],
    tuple(['sensor23','sensor0','sensor22']):['STR-5','2-060A'],
    tuple(['sensor23','sensor21','sensor22']):['2-052'],
    tuple(['sensor21','sensor20','sensor19']):['2-043','2-050','STR-4'],
    tuple(['sensor20','sensor19','sensor18']):['2-048','2-047','2-042'],
    tuple(['sensor16','sensor17','sensor18']):['2-039','2-038','2-037'],
    tuple(['sensor16','sensor17','sensor15']):['2-054'],
    tuple(['sensor13','sensor5','sensor12']):['STR-2'],
    tuple(['sensor6','sensor7','sensor8']):['Pedway','2-001ZZA','2-001','2-001ZZB','2-001ZZC','2-003'],
    tuple(['sensor8','sensor12','sensor9']):['2-001ZZD'],
    tuple(['sensor10','sensor12','sensor9']):['2-010','2-016'],
    tuple(['sensor9','sensor10','sensor11']):['2-020','STR-3']
}

class DataProcessing:
    '''
        Class that processes RSSI data for each sensor group
    '''
    def __init__(self, sensor_group, nodes):
        self.sensorA = all_sensors[sensor_group[0]]
        self.sensorB = all_sensors[sensor_group[1]]
        self.sensorC = all_sensors[sensor_group[2]]
        self.sensor_positions = [self.sensorA.coordinates, self.sensorB.coordinates, self.sensorB.coordinates]
        self.graph = NREFFloor2Graph
        self.node_coordinates = {}
        for node in nodes:
            self.node_coordinates[node] = self.graph.vertices[node].coordinates # graph vertices being monitored by the sensor group

        self.common_devices_keys = self.sensorA.devices.keys() & self.sensorB.devices.keys() & self.sensorC.devices.keys()
        self.common_devices_position = {}
        self.calculate_positions()
        self.process_heat()

    # Calculate the device position using trileration
    def calculate_positions(self):
        for common_device in self.common_devices_keys:
            rssi_A = self.sensorA.devices[common_device]
            distance_A = getSensorDistance(rssi_A)

            rssi_B = self.sensorB.devices[common_device]
            distance_B = getSensorDistance(rssi_B)

            rssi_C = self.sensorC.devices[common_device]
            distance_C = getSensorDistance(rssi_C)

            distances = [distance_A, distance_B, distance_C]

            device_position = trilaterate(self.sensor_positions, distances)
            self.common_devices_position[common_device] = device_position
    
    def process_heat(self):
        for device, position in self.common_devices_position.items():
            correct_node = determine_node(position, self.node_coordinates)
            print("correct node:" + correct_node)
            self.graph.vertices[correct_node].increase_heat()

