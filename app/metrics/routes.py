from fastapi import APIRouter, Request, Depends, Query
from datetime import datetime
from typing import Optional

from app.metrics.schema import EventIn
from app.metrics.services import create_event, get_events, get_event_count
from app.core.database import get_clickhouse_client
from app.core.security import verify_admin_key
from app.services.auth import validate_api_key

router = APIRouter()


@router.post("/event", dependencies=[Depends(validate_api_key)])
async def new_event(request: Request, event: EventIn):
    service = getattr(request.state, "service", None)
    service_id = service.id if service else 0

    event_data = {
        "service_id": service_id,
        "method": request.method,
        "url": request.url.path,
        # Removed cookie collection for privacy and security
        "client_ip": request.client.host if request.client else "",
        "event_type": event.event_type,
        "metadata": event.metadata,
    }

    client = await get_clickhouse_client()
    await create_event(client, event_data)
    return {"status": "ok"}


@router.get("/events", dependencies=[Depends(verify_admin_key)])
async def list_events(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    service_id: Optional[int] = Query(None),
    event_type: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
):
    client = await get_clickhouse_client()
    events = await get_events(
        client,
        limit=limit,
        offset=offset,
        service_id=service_id,
        event_type=event_type,
        start_date=start_date,
        end_date=end_date,
    )
    return events


@router.get("/events/count", dependencies=[Depends(verify_admin_key)])
async def count_events(
    service_id: Optional[int] = Query(None),
    event_type: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
):
    client = await get_clickhouse_client()
    count = await get_event_count(
        client,
        service_id=service_id,
        event_type=event_type,
        start_date=start_date,
        end_date=end_date,
    )
    return {"count": count}
