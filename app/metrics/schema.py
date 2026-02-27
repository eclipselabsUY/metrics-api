from pydantic import BaseModel

class EventIn(BaseModel):
    event_type: str
    metadata: dict | None