import uuid

from sqlalchemy import Column, String, func, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import column_property, relationship

from ..database import Base
from .dish import Dish
from .submenu import Submenu


class Menu(Base):
    __tablename__: str = 'menus'

    id: Column[UUID] = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Column[String] = Column(String, unique=True, index=True)
    description: Column[String] = Column(String)

    submenus: relationship = relationship(
        'Submenu',
        back_populates='menu',
        cascade='all, delete',
    )

    submenus_count: column_property = column_property(
        select([func.count()])
        .where(Submenu.menu_id == id)
        .scalar_subquery()
    )

    dishes_count: column_property = column_property(
        select([func.count()])
        .where(
            Dish.submenu_id.in_(select(Submenu.id).where(Submenu.menu_id == id))
        )
        .scalar_subquery()
    )
