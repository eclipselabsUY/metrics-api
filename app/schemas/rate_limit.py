from pydantic import BaseModel
from typing import Optional


class RateLimitConfigCreate(BaseModel):
    service_id: int
    endpoint_pattern: str = "/"
    max_requests: int = 1000
    window_seconds: int = 3600


class RateLimitConfigUpdate(BaseModel):
    endpoint_pattern: Optional[str] = None
    max_requests: Optional[int] = None
    window_seconds: Optional[int] = None


class RateLimitConfigRead(BaseModel):
    id: int
    service_id: int
    endpoint_pattern: str
    max_requests: int
    window_seconds: int

    model_config = {"from_attributes": True}
