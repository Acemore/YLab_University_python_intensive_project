from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .crud import dish as dish_crud
from .crud import submenu as submenu_crud
from .models.menu import Menu
from .schemas import dish as dish_schema
from .schemas import submenu as submenu_schema


# Используется общий репозиторий на все сущности,
# потому что они образуют общий агрегат:
#  - https://stackoverflow.com/a/2330912
#  - https://martinfowler.com/bliki/DDD_Aggregate.html
class RestaurantRepository:
    def __init__(self, db: Session):
        self.db = db

    # Menu

    def read_menus(self):
        return self.db.query(Menu).all()

    def read_menu(self, menu_id: UUID):
        menu = self.db.query(Menu).get(menu_id)

        if menu is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='menu not found',
            )

        return menu

    def save_menu(self, menu: Menu, is_new: bool):
        if is_new:
            self.db.add(menu)

        self.db.commit()
        self.db.refresh(menu)

        return menu

    def delete_menu(self, menu_id: UUID):
        menu = self.db.query(Menu).get(menu_id)

        if not menu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='menu not found',
            )

        self.db.delete(menu)
        self.db.commit()

        return {'ok': True}

    # Submenu

    def read_submenus(self, menu_id: UUID):
        return submenu_crud.read_submenus(self.db, menu_id)

    def read_submenu(self, menu_id: UUID, submenu_id: UUID):
        return submenu_crud.read_submenu(self.db, menu_id, submenu_id)

    def create_submenu(self, menu_id: UUID, submenu: submenu_schema.SubmenuCreate):
        return submenu_crud.create_submenu(self.db, menu_id, submenu)

    def update_submenu(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        submenu: submenu_schema.SubmenuUpdate,
    ):
        return submenu_crud.update_submenu(self.db, menu_id, submenu_id, submenu)

    def delete_submenu(self, menu_id: UUID, submenu_id: UUID):
        return submenu_crud.delete_submenu(self.db, menu_id, submenu_id)

    # Dish

    def read_dishes(self, submenu_id: UUID):
        return dish_crud.read_dishes(self.db, submenu_id)

    def read_dish(self, submenu_id: UUID, dish_id: UUID):
        return dish_crud.read_dish(self.db, submenu_id, dish_id)

    def create_dish(self, submenu_id: UUID, dish: dish_schema.DishCreate):
        return dish_crud.create_dish(self.db, submenu_id, dish)

    def update_dish(
        self,
        submenu_id: UUID,
        dish_id: UUID,
        dish: dish_schema.DishUpdate,
    ):
        return dish_crud.update_dish(self.db, submenu_id, dish_id, dish)

    def delete_dish(self, submenu_id: UUID, dish_id: UUID):
        return dish_crud.delete_dish(self.db, submenu_id, dish_id)
