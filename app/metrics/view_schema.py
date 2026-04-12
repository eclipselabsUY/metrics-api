from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ViewEventIn(BaseModel):
    path: str = Field(..., max_length=2048, description="URL path")
    referrer: Optional[str] = Field(None, max_length=2048, description="Referrer URL")
    user_agent: Optional[str] = Field(
        None, max_length=512, description="Browser user agent"
    )
    viewport: Optional[str] = Field(
        None, max_length=20, description="Viewport dimensions e.g., 1920x1080"
    )
    document_title: Optional[str] = Field(
        None, max_length=512, description="Page title"
    )
    timestamp: Optional[datetime] = Field(None, description="Client-side timestamp")


class ViewEventOut(BaseModel):
    status: str = "ok"
