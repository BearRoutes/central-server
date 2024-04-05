from fastapi import FastAPI
import asyncio
import asyncpg
from datetime import datetime
import threading

app = FastAPI()

# Database connection pool
pool = None

async def tcp_server():
    server = await asyncio.start_server(handle_client, '0.0.0.0', 50001)

    async with server:
        await server.serve_forever()

async def handle_client_1(reader, writer):
    await handle_client(reader, writer, 'bleber_1_data')

async def handle_client_2(reader, writer):
    await handle_client(reader, writer, 'bleber_2_data')

async def handle_client_3(reader, writer):
    await handle_client(reader, writer, 'bleber_3_data')

async def handle_client(reader, writer, table_name):
    addr = writer.get_extra_info('peername')
    print(f"Connection from {addr}")

    while True:
        data = await reader.readline()
        if not data:
            break
        
        try:
            message = data.decode().strip()
        except:
            continue

        message_array = message.split()
        # print(message)
        if len(message_array) > 12:
            bleber_id = message_array[1]
            device_id = message_array[9]
            radius = message_array[12][:-1]
            now = str(datetime.now())

            sensor_id = ""
            if bleber_id == "1":
                sensor_id = "sensor_0"
            elif bleber_id == "2":
                sensor_id = "sensor_22"
            elif bleber_id == "3":
                sensor_id = "sensor_23"

            # if bleber_id == "1":
            #     sensor_id = "sensor_6"
            # elif bleber_id == "2":
            #     sensor_id == "sensor_7"
            # elif bleber_id == "3":
            #     sensor_id == "sensor_8"
            
            filename = f"bluetooth_data.txt"
            with open(filename, "a") as file:
                file.write(f"{sensor_id}, {device_id}, {radius}, {now}\n")
            print(f"{sensor_id}, {device_id}, {radius}, {now}")
        
        # Echo back to the client
        writer.write(data)
        await writer.drain()

    print("Closing the connection")
    writer.close()

@app.on_event("startup")
async def startup_event():

    # Start separate threads for each socket

    # Used for nrfdevID: 1
    threading.Thread(target=start_tcp_server, args=(handle_client_1, '0.0.0.0', 50001)).start()

    # Used for nrfdevID: 2
    threading.Thread(target=start_tcp_server, args=(handle_client_2, '0.0.0.0', 50002)).start()

    # Used for nfrfdevID: 3
    threading.Thread(target=start_tcp_server, args=(handle_client_3, '0.0.0.0', 50003)).start()

def start_tcp_server(handle_client_func, host, port):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    server = loop.run_until_complete(asyncio.start_server(handle_client_func, host, port))
    try:
        loop.run_forever()
    finally:
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()