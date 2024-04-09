
class Sensor:
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.devices = {} # Device class instances

    def add_device(self, device_address, rssi_array):
        self.devices[device_address] = rssi_array
    
    # Delete device data
    def clear_devices(self):
        self.devices.clear()
    
