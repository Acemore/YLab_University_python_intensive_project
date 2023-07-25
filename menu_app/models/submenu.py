import uuid
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..database import Base


class Submenu(Base):
    __tablename__ = "submenus"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, unique=True, index=True)
    description = Column(String)
    dishes_count = Column(Integer)

    menu_id = Column(
        UUID(as_uuid=True),
        ForeignKey("menus.id", ondelete="CASCADE"),
    )
    menu = relationship("Menu", back_populates="submenus")

    dishes = relationship(
        "Dish",
        back_populates="submenu",
        cascade="all, delete",
    )
