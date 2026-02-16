from fastcrud import crud_router, EndpointCreator
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.core.database import get_async_db
from app.models.service import Service
from app.models.api_key import ApiKey
from app.schemas.services import ServiceCreate, ServiceUpdate
from app.core.security import generate_api_key, hash_api_key, verify_api_key

class ServiceEndpointCreator(EndpointCreator):

    def _create(self):
        async def create_service(data : ServiceCreate, db : AsyncSession = Depends(get_async_db)):
            service = Service(**data.model_dump())
            db.add(service)
            await db.flush()

            raw_key, prefix, secret = generate_api_key()
            hashed = hash_api_key(secret)

            api_key = ApiKey(
                prefix = prefix,
                key_hash=hashed,
                service=service
            )

            db.add(api_key)
            await db.commit()
            await db.refresh(service)

            return {
                "service" : service,
                "api_key" : raw_key # return once
            }
    
        return create_service

service_router = crud_router(session=get_async_db,
                                 model = Service,
                                 create_schema=ServiceCreate,
                                 update_schema=ServiceUpdate,
                                 path="/services",
                                 tags=["Services"],
                                 endpoint_creator=ServiceEndpointCreator
                                 )


async def find_service_by_apikey(db: AsyncSession, raw_api_key: str) -> Service | None:
    
    if not raw_api_key.startswith("egos_"):
        return None
    
    try:
        body = raw_api_key.replace("egos_", "")
        prefix, secret = body.split(".",1)
    
    except ValueError:
        return None
    
    query = select(ApiKey).where(
        ApiKey.prefix == prefix,
        ApiKey.is_active == True
    )

    result = await db.execute(query)
    api_key = result.scalar_one_or_none()

    if not api_key:
        return None
    
    if not verify_api_key(secret, api_key.key_hash):
        return None
    
    return api_key.service