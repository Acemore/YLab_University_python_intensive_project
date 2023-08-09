import uuid

from sqlalchemy import Column, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..database import Base


class Dish(Base):
    __tablename__: str = 'dishes'

    id: Column[UUID] = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Column[String] = Column(String, unique=True, index=True)
    description: Column[String] = Column(String)
    price: Column[Numeric] = Column(Numeric(10, 2))

    submenu_id: Column[UUID] = Column(
        UUID(as_uuid=True),
        ForeignKey('submenus.id', ondelete='CASCADE'),
    )
    submenu: relationship = relationship('Submenu', back_populates='dishes')
