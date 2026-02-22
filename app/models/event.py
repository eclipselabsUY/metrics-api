from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import JSON 

from app.core.database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    event_type_id = Column(Integer, ForeignKey("event_types.id"), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    client_ip = Column(String(45), nullable=True)  # soporta IPv6
    event_metadata = Column(
        JSON, nullable=True
    )  # para Postgres; en SQLite puedes usar JSON o Text

    # Relación con EventType
    event_type = relationship("EventType", back_populates="events")
