from fastcrud import crud_router, EndpointCreator, FastCRUD
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.core.database import get_async_db
from app.models.service import Service, ServiceType
from app.models.api_key import ApiKey
from app.schemas.services import (
    ServiceCreate,
    ServiceUpdate,
    ServiceRead,
    ServiceTypeCreate,
    ServiceTypeUpdate,
    ServiceTypeRead,
)
from app.core.security import generate_api_key, hash_api_key, verify_api_key


class ServiceEndpointCreator(EndpointCreator):
    def _create_service_with_key(self):
        """Custom endpoint that returns API Key"""

        async def create_service(
            data: ServiceCreate, db: AsyncSession = Depends(get_async_db)
        ):
            service = Service(**data.model_dump())
            db.add(service)
            await db.flush()

            raw_key, prefix, secret = generate_api_key()
            hashed = hash_api_key(secret)

            api_key = ApiKey(prefix=prefix, key_hash=hashed, service=service)

            db.add(api_key)
            await db.commit()
            await db.refresh(service)

            return {
                "service": {
                    "id": service.id,
                    "name": service.name,
                    "url": service.url,
                    "service_type_id": service.service_type_id,
                },
                "api_key": raw_key,
            }

        return create_service

    def add_routes_to_router(
        self,
        create_deps=[],
        read_deps=[],
        read_multi_deps=[],
        update_deps=[],
        delete_deps=[],
        db_delete_deps=[],
        included_methods=None,
        deleted_methods=None,
        **kwargs,
    ):
        # Add custom POST /services endpoint (before super() to avoid conflict)
        self.router.add_api_route(
            path="/",
            endpoint=self._create_service_with_key(),
            methods=["POST"],
            response_model=dict,
            tags=self.tags,
            dependencies=create_deps,
        )

        # Call parent with same parameters (will skip 'create' due to deleted_methods)
        super().add_routes_to_router(
            create_deps=create_deps,
            read_deps=read_deps,
            read_multi_deps=read_multi_deps,
            update_deps=update_deps,
            delete_deps=delete_deps,
            db_delete_deps=db_delete_deps,
            included_methods=included_methods,
            deleted_methods=deleted_methods,
        )


service_router = crud_router(
    session=get_async_db,
    model=Service,
    create_schema=ServiceCreate,
    update_schema=ServiceUpdate,
    select_schema=ServiceRead,
    path="",
    tags=["Services"],
    endpoint_creator=ServiceEndpointCreator,
    deleted_methods=["create"],
)

service_type_crud = FastCRUD(ServiceType)

service_type_router = crud_router(
    session=get_async_db,
    model=ServiceType,
    create_schema=ServiceTypeCreate,
    update_schema=ServiceTypeUpdate,
    select_schema=ServiceTypeRead,
    path="/types",
    tags=["ServiceTypes"],
    crud=service_type_crud,
)

service_router.include_router(service_type_router)


async def find_service_by_apikey(db: AsyncSession, raw_api_key: str) -> Service | None:

    if not raw_api_key.startswith("egos_"):
        return None

    try:
        body = raw_api_key.replace("egos_", "")
        prefix, secret = body.split(".", 1)

    except ValueError:
        return None

    query = select(ApiKey).where(ApiKey.prefix == prefix, ApiKey.is_active == True)

    result = await db.execute(query)
    api_key = result.scalar_one_or_none()

    if not api_key:
        return None

    if not verify_api_key(secret, api_key.key_hash):
        return None

    return api_key.service
