from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ClickHousePageView(Base):
    __tablename__ = "page_views"

    id = Column(UUID(as_uuid=True), primary_key=True)
    service_id = Column(Integer, nullable=True)
    path = Column(String(2048), nullable=False)
    referrer = Column(String(2048), nullable=True)
    user_agent = Column(String(512), nullable=True)
    viewport = Column(String(20), nullable=True)
    document_title = Column(String(512), nullable=True)
    client_ip = Column(String(45), nullable=True)
    timestamp = Column(String(32), nullable=True)
