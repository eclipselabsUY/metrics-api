from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.core.enums import ServiceKind

class ServiceType(Base):
    __tablename__ = "service_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    kind = Column(Enum(ServiceKind, name="service_kind_enum"),
        nullable=False,
        index=True,
    )    
    services = relationship(
        "Service",
        back_populates="service_type",
        lazy="selectin"
    )


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    url = Column(String(150))
    api_keys = relationship(
        "ApiKey",
        back_populates="service",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    service_type_id = Column(
        Integer, 
        ForeignKey("service_types.id", ondelete="RESTRICT"), 
        nullable=False
    )
    service_type = relationship(
        "ServiceType",
        back_populates="services",
        lazy="joined"
    )

    def get_type(self) -> str:
        return self.service_type.name
    
    def get_kind(self) -> str:
        return self.service_type.kind.value