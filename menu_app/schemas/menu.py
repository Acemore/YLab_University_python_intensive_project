from uuid import UUID

from pydantic import BaseModel


class MenuBase(BaseModel):
    title: str
    description: str | None = None


class MenuCreate(MenuBase):
    pass


class Menu(MenuBase):
    id: UUID
    submenus_count: int
    dishes_count: int

    class Config:
        orm_mode = True


class MenuUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
