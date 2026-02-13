from fastapi import APIRouter
from app.crud.services import service_router

crud_router = APIRouter()

crud_router.include_router(service_router)