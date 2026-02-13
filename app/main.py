import app.models

from fastapi import FastAPI
from app.status import status_router
from app.middleware.logging import logging_middleware
from app.core.database import async_engine, Base
from app.crud import crud_router

async def lifespan(app: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI()

app.include_router(status_router)

app.include_router(crud_router)

app.middleware("http")(logging_middleware)

@app.get("/")
def base_response():
    return {"message":"Hey! This is EGO Services API. Visit /docs to learn about our API!"}
