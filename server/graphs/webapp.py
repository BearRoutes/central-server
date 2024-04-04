'''
Sources: https://pynative.com/python-get-time-difference/
        https://pypi.org/project/portalocker/
'''

from device_locator import *
from routes import Route
from data_processing import *
from nref_floor2_graph import NREFFloor2Graph
# import asyncio
# import asyncpg
from datetime import datetime, timedelta
import time
import portalocker # pip install portalocker


''' TO BUILD HEAT MAP
STEP 1: Obtain devices detected by a sensor from the database at a certain time frame
'''
# Database connection pool
pool = None

async def clear_database():
    async with pool.acquire() as connection:
        await connection.execute("DELETE FROM device_data")

async def connect_to_db():
    global pool
    pool = await asyncpg.create_pool(
        user='postgres',
        password='BIWiMYaXzIvwsLfmtHhrhJITehjpcCBv',
        database='railway',
        host='viaduct.proxy.rlwy.net',
        port='37675'
    )
async def get_data_from_db(start_timestamp, end_timestamp):

    addr_query = """
        SELECT DISTINCT device_addr
        FROM paulber
        WHERE timestamp BETWEEN 
        CAST($1 AS DATE) AND 
        CAST($2 AS DATE);
        """

    rssi_query = """
        SELECT rssi
        FROM paulber
        WHERE device_name = $1 AND timestamp BETWEEN 
        CAST($1 AS DATE) AND 
        CAST($2 AS DATE);
    """

    # Execute the query asynchronously
    device_addrs = await conn.fetch(query, start_timestamp, end_timestamp)

    for addr in device_addrs:
        pass

    # Close the connection
    await conn.close()

    return results

# # Example usage
# start_timestamp = '2022-01-01 00:00:00'
# end_timestamp = '2022-01-02 00:00:00'
# results = asyncio.run(fetch_data(start_timestamp, end_timestamp))

# # Print the results
# for row in results:
#     print(row)


sensor_data = {}
hour_counter = timedelta(seconds=0).total_seconds()  # Used for clearing BLEBeR data after an hour

def get_data_from_txt():
    global sensor_data, hour_counter
    prev_date_obj = datetime.now()
    total_time = timedelta(seconds=0).total_seconds()
    is_first_line = True

    # hundred_milliseconds = timedelta(milliseconds=100)

    with open('sensor_data.txt', 'r') as file:
        while True:
            line = file.readline()
            if not line:
                # No new line is available, wait before trying to read again
                time.sleep(0.1)
                continue

            line_array = line.strip().split(",")
            # print(f"line array: {line_array}")
            sensor_id = line_array[0]
            device_addr = line_array[1]
            rssi = line_array[2]
            date_str = line_array[3]
            
            # Convert the string to a datetime object
            date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")

            if is_first_line == True:
                prev_date_obj = date_obj
                is_first_line = False
                continue

            # Only collect data within 3 second interval
            delta = date_obj - prev_date_obj
            prev_date_obj = date_obj

            total_time += delta.total_seconds()
            if total_time >= 3:
                print(total_time)
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
        
while True:    

    # If it is one hour  
    if hour_counter >= 10: # Change to 3600
        clear_data()
        for sensor in sensor_data.keys():
            all_sensors[sensor].clear_devices()

    get_data_from_txt()

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
    data_processing = DataProcessing(['sensor0','sensor1','sensor2'], sensor_groups[tuple(['sensor0','sensor1','sensor2'])])
    data_processing = DataProcessing(['sensor3','sensor4','sensor5'], sensor_groups[tuple(['sensor3','sensor4','sensor5'])])



    '''
    STEP 3: Send the graph instance NREFFloor2Graph to the front end to obtain the heat of the vertices

    TODO: Send graph to FastAPI endpoint for the web app front end
    '''
    print(f"HEAT 2-117: {NREFFloor2Graph.vertices['2-117'].heat_level}")
    print(f"HEAT 2-118: {NREFFloor2Graph.vertices['2-118'].heat_level}")
    print(f"HEAT 2-127: {NREFFloor2Graph.vertices['2-127'].heat_level}")
    print(f"HEAT AST-8: {NREFFloor2Graph.vertices['AST-8'].heat_level}")
    print(f"HEAT ELV-179: {NREFFloor2Graph.vertices['ELV-179'].heat_level}")
    print(f"HEAT 2-002ZZ: {NREFFloor2Graph.vertices['2-002ZZ'].heat_level}")
    print(f"HEAT STR-1: {NREFFloor2Graph.vertices['STR-1'].heat_level}")
    print(f"HEAT 2-132: {NREFFloor2Graph.vertices['2-132'].heat_level}")



    
''' PROCESS ROUTE REQUEST'''

''' STEP 1: Get start and destination request from the front end'''
start = '2-118'
destination = '2-090'

''' STEP 2: instantiate Route class '''
route = Route()


''' STEP 3: Calculate route '''
print(route.bfs_route(start, destination))

''' STEP 4: Send to front end '''





    #TODO: SQL command: for each 'sensor' in database, GET detected devices and STORE it in sensor_data dictionary
    #For each device, append device name and RSSIs to devices array
# sensor_data = {'A5:3E:6R:G0':[-50, -48, -46, -47, -43, -44, -44, -42, -40, -42],
#                 'D5:6T:Y7:U8':[-50, -48, -46, -47, -43, -44, -44, -42, -40, -42]}

# sensor_data = {'A5:3E:6R:G0':[-45, -43, -44, -45, -42, -45, -47, -49, -42, -44],
#                 'D5:6T:Y7:U8':[-45, -43, -44, -45, -42, -45, -47, -49, -42, -44]}

# for key, value in sensor_data.items():
#     all_sensors['sensor1'].add_device(key, value)

# sensor_data = {'A5:3E:6R:G0':[-16, -15, -20, -10, -15, -15, -17, -17, -16, -15],
#                 'D5:6T:Y7:U8':[-16, -15, -20, -10, -15, -15, -17, -17, -16, -15]}

# for key, value in sensor_data.items():
#     all_sensors['sensor2'].add_device(key, value)