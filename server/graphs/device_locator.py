'''
Identifies the location of a device using triangulation algorithm

References: 
* An Indoor Positioning Algorithm Using Bluetooth
Low Energy RSSI  by Song Chai, Renbo An and Zhengzhong Du

* https://ieeexplore.ieee.org/document/7275525

* https://www.sciencedirect.com/science/article/pii/S1532046419302072

* Kalman Filter Class: written with assistance of ChatGPT AI tool

'''
import math
import numpy as np


# TODO:Retrieve RSSI values for a device from the database

def getSensorDistance(raw_RSSIs, process_noise=0.1, measurement_error=3, estimate_error=5):
    rssi_p = preprocessRSSI(raw_RSSIs)
    kalman_filter = KalmanFilter(process_noise, measurement_error, estimate_error)
    distance = kalman_filter.calculateDistance(rssi_p)
    return distance


def preprocessRSSI(raw_RSSIs):
    '''
        Preprocesss RSSI Values
        Ten recent RSSI values are stored, and mean (rssi_mean) and standard
        deviation (rssi_std) of these 10 RSSI are calculated. Any RSSI
        that is below (rssi_mean -2*rssi_std) is removed from the
        stored RSSI. Then the average value of the remaining RSSI,
        rssi_p, is the pre-processed RSSI and used in future process. 
    '''
    # Calculate mean
    init_RSSIs = [int(i) for i in raw_RSSIs]
    better_RSSIs = []
    rssi_mean = sum(init_RSSIs)/len(init_RSSIs)
    rssi_std = np.std(init_RSSIs)

    for i in range(len(init_RSSIs)):
        if init_RSSIs[i] >= (rssi_mean - 2*rssi_std):
            better_RSSIs.append(init_RSSIs[i])
    rssi_p = sum(better_RSSIs)/len(better_RSSIs)
    return rssi_p


# # Function to calculate distance from RSSI value
# def RSSI_to_distance(RSSI, RSSI_at_1m=-50, path_loss_exponent=3):
#     """
#     Convert RSSI value to distance using the log-distance path loss model.
#     """
#     distance = 10 ** ((RSSI_at_1m - RSSI) / (10 * path_loss_exponent))
#     return distance

# Function to calculate distance from RSSI value
def RSSI_to_distance(rssi_p, rssi_cali=-50):
    """
        Convert RSSI value to distance
        rssi_p: processed RSSI 
        rssi_cali: RSSI at 1 meter distance
    """
    distance = 1 # rssi_p = rssi_cali

    if (rssi_p > rssi_cali):
        distance = 10 ** (rssi_p/rssi_cali)
    elif (rssi_p < rssi_cali):
        distance = 0.9 * (7.71**(rssi_p/rssi_cali)) + 0.11
    return distance

class KalmanFilter:
    """
        Kalman filtering
        Note: noise and errors varies in different environments, adjust if needed
    """

    def __init__(self, process_noise=0.1, measurement_error=3, estimate_error=5):
        self.distance_estimate = 1
        self.estimate_error = estimate_error
        self.measurement_error = measurement_error
        self.process_noise = process_noise

    def calculateDistance(self, RSSI_measured):
        # Update Kalman Gain
        kalman_gain = self.estimate_error / (self.estimate_error + self.measurement_error)

        # Update distance estimate with the new measurement
        self.distance_estimate += kalman_gain * (RSSI_to_distance(RSSI_measured) - self.distance_estimate)

        # Update the estimate error
        self.estimate_error = (1 - kalman_gain) * self.estimate_error + self.process_noise

        return self.distance_estimate

# Source: https://math.stackexchange.com/questions/884807/find-x-location-using-3-known-x-y-location-using-trilateration
def trilaterate(sensor_positions, device_distances):
    """
    Calculate the device's coordinates using trilateration from three BLEBeRs.

    :param positions: A list of tuples representing the (x, y) coordinates of the BLEBeRs.
    :param distances: A list of distances from each BLEBeRs to the device.
    :return: The estimated (x, y) coordinates of the device.
    """
    # Unpack the positions and distances
    (x1, y1), (x2, y2), (x3, y3) = sensor_positions
    r1, r2, r3 = device_distances
    try:
        # Using the mathematics of trilateration
        A = 2*x2 - 2*x1
        B = 2*y2 - 2*y1
        C = r1**2 - r2**2 - x1**2 + x2**2 - y1**2 + y2**2
        D = 2*x3 - 2*x2
        E = 2*y3 - 2*y2
        F = r2**2 - r3**2 - x2**2 + x3**2 - y2**2 + y3**2

        # Calculate the device's coordinates
        x = (C*E - F*B) / (E*A - B*D)
        y = (C*D - A*F) / (B*D - A*E)

        return x, y
    except:
        print("Trilateration cannot be performed")
        return x1, y1


# TODO: Get RSSIs from the database
# vertex candidates: array of vertex classes with their coordinates
# vertex candidates and sensor targets should refer to the same thing for a sensor group
def determine_node(device_position, vertex_candidates):
    shortest_distance = 100000
    correct_vertex = ""
    for vertex_name, coordinate in vertex_candidates.items():
        manhattan_distance = abs(device_position[0]*100-coordinate[0]*100) + abs(device_position[1]*100-coordinate[1]*100)
        if manhattan_distance < shortest_distance:
            shortest_distance = manhattan_distance
            correct_vertex = vertex_name
    return correct_vertex

# Example usage
# Sensor 1
# recent_RSSIs = [-50, -48, -46, -47, -43, -44, -44, -42, -40, -42]
# distance_1 = getSensorDistance(recent_RSSIs)

# # Sensor 2
# recent_RSSIs = [-30, -28, -36, -40, -31, -32, -36, -30, -32, -28]
# distance_2 = getSensorDistance(recent_RSSIs)

# # Sensor 3
# recent_RSSIs = [-50, -48, -46, -47, -43, -44, -44, -42, -40, -42]
# distance_3 = getSensorDistance(recent_RSSIs)

# distances = [distance_1, distance_2, distance_3]
# print(f"distances:{distances}\n")

# sensor_positions = [(37.2, 61.2), (45.9, 65), (48.5, 59)]  # Example beacon positions

# device_position = trilaterate(sensor_positions, distances)
# print(f"Device is located at: {device_position}")


# candidates = {
#                 '2-125':(53.1937,64.2512), 
#                 '2-118':(38.5264,62.8370),
#                 '2-117':(44.1450,64.0992)
#             }

# device_position = (41.9536,64.1992)

# correct_vertex = determine_node(device_position,candidates)
# # print(correct_vertex)

# device_position = (37.5410,58.3692)

# correct_vertex = determine_node(device_position,candidates)
# # print(correct_vertex)

# device_position = (56.6003,56.5452)

# correct_vertex = determine_node(device_position,candidates)
# print(correct_vertex)

# Increase heat
# NREFFloor2Graph.vertices[correct_vertex].increase_heat()
# heat = NREFFloor2Graph.vertices[correct_vertex].heat_level
# print(f"graph {heat}")






