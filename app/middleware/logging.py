import time
from fastapi import Request

from app.logging import logger

async def logging_middleware(request: Request, call_next):
    start = time.time()
    
    response  = await call_next(request)

    duration = round((time.time() - start) * 1000, 2)

    logger.info(
        "HTTP request",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status": response.status_code,
            "client": request.client.host if request.client else None,
            "duration_ms": duration,
        },
    )

    return response