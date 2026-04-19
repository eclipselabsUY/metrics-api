from pydantic import BaseModel, Field
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.event import EventRead


class EventTypeCreate(BaseModel):
    name: str
    description: str
    service_id: int


class EventTypeUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]


class EventTypeRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    events: List["EventRead"] = Field(default_factory=list)
    service_id: int

    class Config:
        from_attributes = True


from app.schemas.event import EventRead

EventTypeRead.model_rebuild()
