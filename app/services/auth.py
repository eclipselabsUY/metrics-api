from fastapi import Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.services import find_service_by_apikey

from app.core.database import get_async_db


def validate_api_key(request: Request, db: AsyncSession = Depends(get_async_db)):
    api_key = request.headers.get("X-API-Key")

    if not api_key:
        raise HTTPException(401)

    service = find_service_by_api_key(db, api_key)

    if not service:
        raise HTTPException(403)

    request.state.service = service
