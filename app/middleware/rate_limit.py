import time
import uuid
import logging
from fastapi import Request, HTTPException
from starlette.responses import JSONResponse
import redis.asyncio as aioredis

from app.core.config import (
    RATE_LIMIT_DEFAULT,
    RATE_LIMIT_WINDOW,
    RATE_LIMIT_BLOCK_AFTER,
)
from app.core.database import get_redis_client

logger = logging.getLogger(__name__)


def _get_client_ip(request: Request) -> str:
    return request.client.host if request.client else "unknown"


async def check_rate_limit(request: Request, redis: aioredis.Redis, identifier: str):
    now = time.time()
    window_start = now - RATE_LIMIT_WINDOW

    key = f"rl:{identifier}"
    block_key = f"rl:block:{identifier}"
    violations_key = f"rl:violations:{identifier}"

    is_blocked = await redis.get(block_key)
    if is_blocked:
        retry_after = await redis.ttl(block_key)
        if retry_after < 0:
            retry_after = RATE_LIMIT_WINDOW
        raise HTTPException(
            status_code=429,
            detail={
                "error": "Too Many Requests",
                "message": "You have been rate limited and blocked due to repeated violations",
                "retry_after": retry_after,
            },
        )

    await redis.zremrangebyscore(key, 0, window_start)

    current_count = await redis.zcard(key)

    if current_count >= RATE_LIMIT_DEFAULT:
        consecutive_violations = await redis.incr(violations_key)
        await redis.expire(violations_key, RATE_LIMIT_WINDOW)
        if consecutive_violations >= RATE_LIMIT_BLOCK_AFTER:
            block_duration = RATE_LIMIT_WINDOW * 4
            await redis.set(block_key, "1", ex=block_duration)
            await redis.delete(violations_key)
            raise HTTPException(
                status_code=429,
                detail={
                    "error": "Too Many Requests",
                    "message": "Blocked due to repeated rate limit violations",
                    "retry_after": block_duration,
                },
            )
        raise HTTPException(
            status_code=429,
            detail={
                "error": "Too Many Requests",
                "message": f"Rate limit exceeded. {RATE_LIMIT_DEFAULT} requests per {RATE_LIMIT_WINDOW}s window",
                "retry_after": RATE_LIMIT_WINDOW,
            },
        )

    await redis.delete(violations_key)

    if current_count == 0:
        await redis.expire(key, RATE_LIMIT_WINDOW)

    member = f"{now}:{uuid.uuid4().hex[:8]}"
    await redis.zadd(key, {member: now})
    await redis.expire(key, RATE_LIMIT_WINDOW)

    remaining = RATE_LIMIT_DEFAULT - current_count - 1

    return remaining


async def rate_limit_middleware(request: Request, call_next):
    api_key = request.headers.get("X-API-Key")

    # Check if we should exempt authenticated requests from rate limiting
    if api_key and api_key.startswith("egos_"):
        # Validate the API key by attempting to find the service
        from app.crud.services import find_service_by_apikey
        from app.core.database import get_async_db

        try:
            # Get database session and validate the API key
            async for db in get_async_db():
                service = await find_service_by_apikey(db, api_key)
                if service:
                    # Valid API key - exempt from rate limiting
                    return await call_next(request)
                break  # Exit the async for loop after first iteration
        except Exception as e:
            logger.error(f"API key validation failed: {e}")
            # Fall through to IP-based rate limiting on validation error

    client_ip = _get_client_ip(request)
    identifier = f"ip:{client_ip}"
    remaining = 0

    try:
        redis = await get_redis_client()
        remaining = await check_rate_limit(request, redis, identifier)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Rate limit check failed: {e}")
        remaining = 0

    response = await call_next(request)

    response.headers["X-RateLimit-Limit"] = str(RATE_LIMIT_DEFAULT)
    response.headers["X-RateLimit-Remaining"] = str(max(0, remaining))
    response.headers["X-RateLimit-Window"] = str(RATE_LIMIT_WINDOW)

    return response
