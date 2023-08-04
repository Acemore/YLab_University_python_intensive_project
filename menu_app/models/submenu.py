import uuid

from sqlalchemy import Column, ForeignKey, String, func, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import column_property, relationship

from ..database import Base
from .dish import Dish


class Submenu(Base):
    __tablename__ = 'submenus'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, unique=True, index=True)
    description = Column(String)

    menu_id = Column(
        UUID(as_uuid=True),
        ForeignKey('menus.id', ondelete='CASCADE'),
    )
    menu = relationship('Menu', back_populates='submenus')

    dishes = relationship(
        'Dish',
        back_populates='submenu',
        cascade='all, delete',
    )

    dishes_count = column_property(
        select([func.count()])
        .where(Dish.submenu_id == id)
        .scalar_subquery()
    )
