from fastcrud import crud_router as fastcrud_router

from app.core.database import get_async_db
from app.models.service import Service
from app.schemas.services import ServiceCreate, ServiceUpdate

service_router = fastcrud_router(session=get_async_db,
                                 model = Service,
                                 create_schema=ServiceCreate,
                                 update_schema=ServiceUpdate,
                                 path="/services",
                                 tags=["Services"])