from pydantic import BaseModel, Field
from typing import TYPE_CHECKING, Optional
from datetime import datetime

if TYPE_CHECKING:
    from app.schemas.event_type import EventTypeRead


class EventCreate(BaseModel):
    event_type_id: int
    event_metadata: dict = Field(default_factory=dict)


class EventUpdate(BaseModel):
    client_ip: Optional[str] = None
    event_metadata: Optional[dict] = None


class EventRead(BaseModel):
    id: int
    event_type: "EventTypeRead"
    timestamp: datetime
    client_ip: str
    event_metadata: dict


from app.schemas.event_type import EventTypeRead

EventRead.model_rebuild()
