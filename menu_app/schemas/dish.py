from pydantic import BaseModel
from uuid import UUID


class DishBase(BaseModel):
    title: str
    description: str | None = None
    price: str


class DishCreate(DishBase):
    pass


class Dish(DishBase):
    id: UUID
    submenu_id: UUID

    class Config:
        orm_mode: True


class DishUpdate(BaseModel):
    title: str = None
    description: str | None = None
    price: str = None
