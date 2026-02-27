from fastcrud import crud_router, FastCRUD

from app.core.database import get_async_db
from app.schemas.event_type import EventTypeCreate, EventTypeRead, EventTypeUpdate
from app.models.event_type import EventType

event_type_crud = FastCRUD(EventType)

event_type_router = crud_router(
    session=get_async_db,
    model=EventType,
    create_schema=EventTypeCreate,
    update_schema=EventTypeUpdate,
    select_schema=EventTypeRead,
    crud=event_type_crud,
    path="",
    endpoint_names={"read" : "get", "read_multi" : "get", "update" : "update", "delete" : "delete", "create" : "create"},
    tags=["EventType"]
)
