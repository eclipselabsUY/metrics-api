from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.event import Event

class EventType(Base):
    __tablename__ = "event_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=True)

    # Relación con Event
    events = relationship("Event", back_populates="event_type", lazy="selectin")