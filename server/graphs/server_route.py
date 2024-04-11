from fastapi import FastAPI
from pydantic import BaseModel
from device_locator import *
from routes import Route
from data_processing import *
from datetime import datetime, timedelta
import time
import json
import portalocker
from nref_floor2_graph import NREFFloor2Graph
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Query

# pip install fastapi uvicorn
# python -m uvicorn server_route:app
# http://localhost:8000/route?start=2-118&end=2-001
# http://localhost:8000/heat?timestamp=2024-04-10T15:30:00-06:00
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
    date = datetime.fromisoformat(timestamp)

    # Extract the month, day, and time
    month = str(date.month)
    day = str(date.weekday())
    time_string = f"{date.hour}00"

    heat_json = {}

    with open('heat_data.json', 'r') as file:
        heat_json = json.load(file)

    return heat_json[month][day][time_string]

@app.on_event("shutdown")
async def shutdown_event():
    # Perform cleanup tasks here
    pass