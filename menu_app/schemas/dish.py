from uuid import UUID

from pydantic import BaseModel


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
        orm_mode: bool = True


class DishUpdate(BaseModel):
    title: str
    description: str | None = None
    price: str | None = None
