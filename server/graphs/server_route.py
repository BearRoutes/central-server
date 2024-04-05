from fastapi import FastAPI
from pydantic import BaseModel
from nref_floor2_graph import NREFFloor2Graph

# pip install fastapi uvicorn
# python -m uvicorn server_route:app
# http://localhost:8000/route?start=2-118&end=2-001
app = FastAPI()

@app.get("/route")
async def get_route(start: str, end: str):
    route_class = Route()
    route = route_class.bfs_route(start, end)
    return {"route": route}

@app.get("/heat")
async def get_graph():
    heat_levels = {}
    for vertex_id, vertex_class in NREFFloor2Graph.vertices.items():
        heat_levels[vertex_id] = vertex_class.heat_level
    return {"heat": heat_levels}
