from fastapi import FastAPI
from pydantic import BaseModel
from device_locator import *
from routes import Route
from data_processing import *
from datetime import datetime, timedelta
import time
import portalocker
from nref_floor2_graph import NREFFloor2Graph
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Query

# pip install fastapi uvicorn
# python -m uvicorn server_route:app
# http://localhost:8000/route?start=2-118&end=2-001
# http://localhost:8000/heat
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origins in production
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

sensor_data = {}

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return PlainTextResponse("")

@app.get("/route")
async def get_route(start: str, end: str):
    route_class = Route()
    route = route_class.bfs_route(start, end)
    return {"route": route}

@app.get("/heat")
async def get_heat(timestamp: str = Query(None)):
    # return {"heat":{"2-125":66,"2-118":0,"2-117":66,"STR-1":0,"2-002ZZ":3,"ELV-179":19,"2-132":0,"AST-8":0,"2-001":1,"Pedway":2,"2-001ZZA":0,"2-003":23,"2-011":44,"STR-6":4,"STR-2":66,"2-005ZZB":43,"ELV-18X":19,"2-054":66,"2-047":16,"STR-4":23,"2-050":42,"2-052":0,"2-043":1,"2-048":30,"2-042":20,"2-039":20,"2-038":5,"2-037":41,"2-090":0,"2-060C":0,"2-005ZZA":0,"2-060B":0,"2-060A":0,"STR-5":0,"STR-3":1,"2-020":65,"2-016":30,"2-010":36,"2-001ZZD":66,"2-001ZZC":31,"2-001ZZB":9,"2-002":21,"AST-2-132":1,"2-127":44}
    #         ,"data": timestamp}

    global sensor_data
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

    clear_data()
    for sensor in sensor_data.keys():
        all_sensors[sensor].clear_devices()
    
    print(f"HEAT 2-060A: {NREFFloor2Graph.vertices['2-060A'].heat_level}")
    heat_levels = {}
    for vertex_id, vertex_class in NREFFloor2Graph.vertices.items():
        heat_levels[vertex_id] = vertex_class.heat_level
    return {"heat": heat_levels}


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
            try:
                # print(f"line array: {line_array}")
                sensor_id = line_array[0].strip()
                device_addr = line_array[1].strip()
                rssi = line_array[2].strip()
                date_str = line_array[3].strip()
            except IndexError:
                continue

            
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
            if total_time >= 10:
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

@app.on_event("shutdown")
async def shutdown_event():
    # Perform cleanup tasks here
    pass