from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ClickHouseEvent(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True)
    service_id = Column(Integer, nullable=True)
    event_type = Column(String(255), nullable=False)
    method = Column(String(16), nullable=True)
    url = Column(String(2048), nullable=True)
    client_ip = Column(String(45), nullable=True)
    event_metadata = Column(String(65535), nullable=True)
    timestamp = Column(String(32), nullable=True)
