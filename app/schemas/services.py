from pydantic import BaseModel

class ServiceCreate(BaseModel):
    name: str
    url: str
    service_type_id: int


class ServiceUpdate(BaseModel):
    name: str | None = None
    url: str | None = None
    service_type_id: int | None = None