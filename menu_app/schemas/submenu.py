from uuid import UUID

from pydantic import BaseModel


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
        orm_mode: bool = True


class SubmenuUpdate(BaseModel):
    title: str
    description: str | None = None
