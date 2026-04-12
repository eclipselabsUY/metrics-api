from fastapi import APIRouter, Request, Depends, Query
from datetime import datetime
from typing import Optional

from app.metrics.view_schema import ViewEventIn
from app.metrics.services import (
    create_view_event,
    get_views,
    get_view_stats,
    get_view_count,
    get_views_timeline,
)
from app.core.database import get_clickhouse_client
from app.core.security import verify_admin_key
from app.services.auth import validate_api_key

router = APIRouter()


@router.post("/views", dependencies=[Depends(validate_api_key)])
async def new_view(request: Request, view: ViewEventIn):
    service = getattr(request.state, "service", None)
    service_id = service.id if service else 0

    view_data = {
        "service_id": service_id,
        "path": view.path,
        "referrer": view.referrer or "",
        "user_agent": view.user_agent or "",
        "viewport": view.viewport or "",
        "document_title": view.document_title or "",
        "client_ip": request.client.host if request.client else "",
        "timestamp": view.timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        if view.timestamp
        else None,
    }

    client = await get_clickhouse_client()
    await create_view_event(client, view_data)
    return {"status": "ok"}


@router.get("/views", dependencies=[Depends(verify_admin_key)])
async def list_views(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    service_id: Optional[int] = Query(None),
    path: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
):
    client = await get_clickhouse_client()
    views = await get_views(
        client,
        limit=limit,
        offset=offset,
        service_id=service_id,
        path=path,
        start_date=start_date,
        end_date=end_date,
    )
    return views


@router.get("/views/stats", dependencies=[Depends(verify_admin_key)])
async def view_stats(
    service_id: Optional[int] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
):
    client = await get_clickhouse_client()
    stats = await get_view_stats(
        client,
        service_id=service_id,
        start_date=start_date,
        end_date=end_date,
    )
    return stats


@router.get("/views/count", dependencies=[Depends(verify_admin_key)])
async def count_views(
    service_id: Optional[int] = Query(None),
    path: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
):
    client = await get_clickhouse_client()
    count = await get_view_count(
        client,
        service_id=service_id,
        path=path,
        start_date=start_date,
        end_date=end_date,
    )
    return {"count": count}


@router.get("/views/timeline", dependencies=[Depends(verify_admin_key)])
async def views_timeline(
    service_id: Optional[int] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    interval_hours: int = Query(1, ge=1, le=24),
):
    client = await get_clickhouse_client()
    timeline = await get_views_timeline(
        client,
        service_id=service_id,
        start_date=start_date,
        end_date=end_date,
        interval_hours=interval_hours,
    )
    return timeline
