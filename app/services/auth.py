from fastapi import Request, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.services import find_service_by_api_key

from app.core.database import get_sync_db

def validate_api_key(request: Request, db : Session = Depends(get_sync_db)):
    api_key = request.headers.get("X-API-Key")

    if not api_key:
        raise HTTPException(401)
    
    service = find_service_by_api_key(db, api_key)

    if not service:
        raise HTTPException(403)
    
    request.state.service = service