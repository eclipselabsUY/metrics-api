from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base


class ApiKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)

    # hash Argon2 de la key
    key_hash = Column(String(255), nullable=False, unique=True)

    service_id = Column(
        Integer,
        ForeignKey("services.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    service = relationship(
        "Service",
        back_populates="api_keys",
        lazy="joined"
    )

    is_active = Column(Boolean, default=True, nullable=False)
