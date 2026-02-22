from pydantic import BaseModel, Field
from typing import Dict, TYPE_CHECKING, List, Any
from datetime import datetime

if TYPE_CHECKING:
    from app.schemas.event_type import EventTypeRead

class EventCreate(BaseModel):
    client_ip : str
    event_metadata : Dict[str, Any]

class EventRead(BaseModel):
    id : int
    event_type : "EventTypeRead"
    timestamp : datetime
    client_ip : str
    event_metadata : Dict[str, Any]

from app.schemas.event_type import EventTypeRead

EventRead.model_rebuild()