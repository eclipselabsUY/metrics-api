from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class RateLimitConfig(Base):
    __tablename__ = "rate_limit_configs"

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(
        Integer,
        ForeignKey("services.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    endpoint_pattern = Column(String(255), nullable=False, default="/")
    max_requests = Column(Integer, nullable=False, default=1000)
    window_seconds = Column(Integer, nullable=False, default=3600)

    service = relationship("Service", back_populates="rate_limits", lazy="joined")
