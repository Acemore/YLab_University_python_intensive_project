from pydantic import BaseModel
from uuid import UUID


class SubmenuBase(BaseModel):
    title: str
    description: str | None = None


class SubmenuCreate(SubmenuBase):
    pass


class Submenu(SubmenuBase):
    id: UUID
    menu_id: UUID
    dishes_count: int

    class Config:
        orm_mode: True


class SubmenuUpdate(BaseModel):
    title: str = None
    description: str | None = None
