from fastapi import APIRouter
import asyncio
import os
import rcon

from app.helpers import check_http, check_tcp
from app.config import SERVICES

router = APIRouter()

@router.get("/status")
async def services_status():
    response = []

    tasks = []
    for service in SERVICES:
        if service["type"] == "http":
            tasks.append(check_http(service))
        else:
            tasks.append(check_tcp(service))
    
    results = await asyncio.gather(*tasks)

    for i, service in enumerate(SERVICES):
        response.append({
            "service": service["name"],
            "status": results[i]
        })

    return response
        

@router.get("/fingcraft-stats")
async def fingcraft_status():

    response = []

    with rcon.Client("fingcraft", 25575, passwd=os.getenv("RCON_PASSWORD")) as client:
        response.append({"current_players": await asyncio.to_thread(client.run, "list")})
        response.append({"time": await asyncio.to_thread(client.run, "time")})
        response.append({"stats": await asyncio.to_thread(client.run, "memory")})
        response.append({"version": await asyncio.to_thread(client.run, "version")})

    return response

@router.get("/health")
def health_point():
    return {"status_code" : "200"}