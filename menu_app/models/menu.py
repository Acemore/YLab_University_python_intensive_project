import uuid
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..database import Base


class Menu(Base):
    __tablename__ = "menus"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, unique=True, index=True)
    description = Column(String)
    submenus_count = Column(Integer)
    dishes_count = Column(Integer)

    submenus = relationship(
        "Submenu",
        back_populates="menu",
        cascade="all, delete",
    )
