from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class ServiceType(Base):
    __tablename__ = "service_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
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
    service_type_id = Column(
        Integer, 
        ForeignKey("services_types.id", ondelete="RESTRICT"), 
        nullable=False
    )
    service_type = relationship(
        "ServiceType",
        back_populates="services",
        lazy="joined"
    )

    def get_type(self) -> str:
        return self.service_type.name