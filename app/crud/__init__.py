from fastapi import APIRouter
from app.crud.services import service_router, service_type_router
from app.crud.event_types import event_type_router
from app.crud.events import event_router

crud_router = APIRouter()

crud_router.include_router(service_router, prefix="/services")
crud_router.include_router(event_type_router, prefix="/event-types")
crud_router.include_router(event_router, prefix="/events")
