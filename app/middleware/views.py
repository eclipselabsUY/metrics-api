import logging
import os
from datetime import datetime
from fastapi import Request
from app.core.database import get_clickhouse_client
from app.metrics.services import create_view_event

logger = logging.getLogger(__name__)

VIEW_TRACKING_ENABLED = os.getenv("VIEW_TRACKING_ENABLED", "true").lower() == "true"
VIEW_TRACKING_SAMPLE_RATE = float(os.getenv("VIEW_TRACKING_SAMPLE_RATE", "1.0"))

EXCLUDED_PATHS = {
    "/",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/health",
    "/metrics",
    "/event",
    "/events",
    "/events/count",
}

EXCLUDED_EXTENSIONS = {
    ".js",
    ".css",
    ".ico",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
    ".woff",
    ".woff2",
    ".ttf",
    ".eot",
}


async def view_tracking_middleware(request: Request, call_next):
    if not VIEW_TRACKING_ENABLED:
        return await call_next(request)

    path = request.url.path

    if path in EXCLUDED_PATHS:
        return await call_next(request)

    ext = os.path.splitext(path)[1].lower()
    if ext in EXCLUDED_EXTENSIONS:
        return await call_next(request)

    import random

    if random.random() > VIEW_TRACKING_SAMPLE_RATE:
        return await call_next(request)

    user_agent = request.headers.get("user-agent", "")
    if (
        "bot" in user_agent.lower()
        or "spider" in user_agent.lower()
        or "crawler" in user_agent.lower()
    ):
        return await call_next(request)

    referer = request.headers.get("referer", "")

    response = await call_next(request)

    if response.status_code >= 200 and response.status_code < 400:
        try:
            service_id = 0
            service = getattr(request.state, "service", None)
            if service:
                service_id = service.id

            view_data = {
                "service_id": service_id,
                "path": path,
                "referrer": referer,
                "user_agent": user_agent,
                "viewport": "",
                "document_title": "",
                "client_ip": request.client.host if request.client else "",
                "timestamp": None,
            }

            client = await get_clickhouse_client()
            await create_view_event(client, view_data)
        except Exception as e:
            logger.error(f"View tracking failed: {e}")

    return response
