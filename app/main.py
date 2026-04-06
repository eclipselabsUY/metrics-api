import app.models

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.status import status_router
from app.middleware.logging import logging_middleware
from app.core.database import (
    async_engine,
    Base,
    get_clickhouse_client,
    close_clickhouse_client,
)
from app.crud import crud_router
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


app = FastAPI(lifespan=lifespan)

app.include_router(status_router)

app.include_router(crud_router)

app.include_router(metrics_router, prefix="/metrics", tags=["Metrics"])

app.middleware("http")(logging_middleware)


@app.get("/")
def base_response():
    return {
        "message": "Hey! This is Eclipse Labs API. Visit /docs to learn about our API!"
    }
