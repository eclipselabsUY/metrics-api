from fastcrud import crud_router, FastCRUD

from app.core.database import get_async_db
from app.schemas.event_type import EventTypeCreate, EventTypeRead, EventTypeUpdate
from app.models.api.event_type import EventType
from app.core.security import verify_admin_key

event_type_crud = FastCRUD(EventType)

event_type_router = crud_router(
    session=get_async_db,
    model=EventType,
    create_schema=EventTypeCreate,
    update_schema=EventTypeUpdate,
    select_schema=EventTypeRead,
    crud=event_type_crud,
    path="",
    endpoint_names={
        "read": "get",
        "read_multi": "get",
        "update": "update",
        "delete": "delete",
        "create": "create",
    },
    tags=["EventType"],
    create_deps=[verify_admin_key],
    update_deps=[verify_admin_key],
    delete_deps=[verify_admin_key],
    read_deps=[verify_admin_key],
    read_multi_deps=[verify_admin_key],
)
