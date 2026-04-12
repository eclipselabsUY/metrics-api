from pydantic import BaseModel

from pydantic import BaseModel, Field
from typing import Dict, Optional


class EventIn(BaseModel):
    event_type: str = Field(..., max_length=255, description="Event type identifier")
    metadata: Optional[Dict[str, str]] = Field(default=None, max_items=50)
