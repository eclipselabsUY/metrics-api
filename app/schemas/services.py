from pydantic import BaseModel, field_validator, HttpUrl
from typing import Optional, List

from app.core.enums import ServiceKind


class ServiceCreate(BaseModel):
    name: str
    url: str
    service_type_id: int


class ServiceUpdate(BaseModel):
    name: str | None = None
    url: str | None = None
    service_type_id: int | None = None


class ServiceRead(BaseModel):
    id: int
    name: str
    url: str
    service_type_id: int


class ServiceTypeCreate(BaseModel):
    name: str
    kind: ServiceKind

    @field_validator("kind", mode="before")
    def normalize_kind(cls, v):
        if isinstance(v, str):
            return v.lower()
        return v


class ServiceTypeUpdate(BaseModel):
    name: Optional[str]
    kind: Optional[ServiceKind]

    @field_validator("kind", mode="before")
    def normalize_kind(cls, v):
        if isinstance(v, str):
            return v.lower()
        return v


class ServiceTypeRead(BaseModel):
    id: int
    name: str
    services: List[ServiceRead] = []
