from fastapi import FastAPI
import logging
from httpx import RequestError, AsyncClient
import asyncio
import rcon
import os
from dotenv import load_dotenv

app = FastAPI()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# ENV VAR

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

# Variables

SERVICES = [
    {"name": "www.ego-services.com", "type": "http", "url": "https://www.ego-services.com"},
    {"name": "backdoor.ego-services.com", "type": "http", "url": "https://backdoor.ego-services.com/health"},
    {"name": "fingcraft.ego-services.com", "type": "tcp", "host": "fingcraft.ego-services.com", "port": 25565},
    {"name": "ssh.ego-services.com", "type": "tcp", "host": "ssh.ego-services.com", "port": 22},
]

@app.get("/")
def base_response():
    return {"message":"Hey! This is EGO Services API. Visit /docs to learn about our API!"}

async def check_http(service):
    async with AsyncClient() as client:
        try:
            r = await client.get(service["url"])
            return "Healthy" if r.status_code == 200 else "Degraded"

        except RequestError:
            return "Degraded"

async def check_tcp(service):
    try:
        reader, writer = await asyncio.open_connection(service["host"], service["port"])
        writer.close()
        await writer.wait_closed()
        return "Healthy"
    except Exception:
        return "Degraded"

@app.get("/status")
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
        

@app.get("/fingcraft-stats")
async def fingcraft_status():

    response = []
    
    with rcon.Client("fingcraft", 25575, passwd=os.getenv("RCON_PASSWORD")) as client:
        response.append({"current_players" : await asyncio.to_thread(client.run("list"))})
        response.append({"time" : await asyncio.to_thread(client.run("time"))})
        response.append({"stats" : await asyncio.to_thread(client.run("memory"))})
        response.append({"version" : await asyncio.to_thread(client.run("version"))})

    return response