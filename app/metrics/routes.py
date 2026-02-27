from fastapi import APIRouter, Request, Depends

from app.metrics.schema import EventIn
from app.metrics.services import create_event
from app.services.auth import validate_api_key

router = APIRouter()

@router.post("/event", dependencies=Depends(validate_api_key))
async def new_event(request : Request, event : EventIn):
    event_data = {
        "method" : request.method,
        "url" : request.url.path,
        "cookies" : request.cookies,
        "client_ip" : request.client.host,
        "event_type" : event.event_type,
        "metadata" : event.metadata 
    }

    create_event(event_data)