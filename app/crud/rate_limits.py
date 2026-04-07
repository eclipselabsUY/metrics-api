from fastcrud import crud_router, FastCRUD

from app.core.database import get_async_db
from app.models.rate_limit import RateLimitConfig
from app.schemas.rate_limit import (
    RateLimitConfigCreate,
    RateLimitConfigRead,
    RateLimitConfigUpdate,
)
from app.core.security import verify_admin_key

rate_limit_crud = FastCRUD(RateLimitConfig)

rate_limit_router = crud_router(
    session=get_async_db,
    model=RateLimitConfig,
    create_schema=RateLimitConfigCreate,
    update_schema=RateLimitConfigUpdate,
    select_schema=RateLimitConfigRead,
    crud=rate_limit_crud,
    path="",
    endpoint_names={
        "read": "get",
        "read_multi": "get",
        "update": "update",
        "delete": "delete",
        "create": "create",
    },
    tags=["RateLimits"],
    create_deps=[verify_admin_key],
    update_deps=[verify_admin_key],
    delete_deps=[verify_admin_key],
    read_deps=[verify_admin_key],
    read_multi_deps=[verify_admin_key],
)
