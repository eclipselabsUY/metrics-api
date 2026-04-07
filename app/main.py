import app.models

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.status import status_router
from app.middleware.logging import logging_middleware
from app.middleware.rate_limit import rate_limit_middleware
from app.core.database import (
    async_engine,
    Base,
    get_clickhouse_client,
    close_clickhouse_client,
    close_redis_client,
)
from app.crud import crud_router
from app.crud.rate_limits import rate_limit_router
from app.metrics import metrics_router
from app.metrics.services import init_clickhouse


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    client = await get_clickhouse_client()
    await init_clickhouse(client)
    yield
    await close_clickhouse_client()
    await close_redis_client()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(rate_limit_middleware)

app.include_router(status_router)

app.include_router(crud_router)

app.include_router(rate_limit_router, prefix="/rate-limits", tags=["RateLimits"])

app.include_router(metrics_router, prefix="/metrics", tags=["Metrics"])

app.middleware("http")(logging_middleware)


@app.get("/")
def base_response():
    return {
        "message": "Hey! This is Eclipse Labs API. Visit /docs to learn about our API!"
    }
