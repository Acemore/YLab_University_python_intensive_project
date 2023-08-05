from uuid import UUID

from sqlalchemy.orm import Session

from .crud import dish as dish_crud
from .crud import menu as menu_crud
from .crud import submenu as submenu_crud
from .schemas import dish as dish_schema
from .schemas import menu as menu_schema
from .schemas import submenu as submenu_schema

cache = dict()


class RestaurantRepository:
    def __init__(self, db: Session):
        self.db = db

    def read_menus(self):
        return menu_crud.read_menus(self.db)

    def read_submenus(self, menu_id: UUID):
        return submenu_crud.read_submenus(self.db, menu_id)

    def read_dishes(self, submenu_id: UUID):
        return dish_crud.read_dishes(self.db, submenu_id)

    def read_menu(self, menu_id: UUID):
        return menu_crud.read_menu(self.db, menu_id)

    def read_submenu(self, menu_id: UUID, submenu_id: UUID):
        return submenu_crud.read_submenu(self.db, menu_id, submenu_id)

    def read_dish(self, submenu_id: UUID, dish_id: UUID):
        return dish_crud.read_dish(self.db, submenu_id, dish_id)

    def create_menu(self, menu: menu_schema.MenuCreate):
        return menu_crud.create_menu(self.db, menu)

    def create_submenu(self, menu_id: UUID, submenu: submenu_schema.SubmenuCreate):
        return submenu_crud.create_submenu(self.db, menu_id, submenu)

    def create_dish(self, submenu_id: UUID, dish: dish_schema.DishCreate):
        return dish_crud.create_dish(self.db, submenu_id, dish)

    def update_menu(self, menu_id: UUID, menu: menu_schema.MenuUpdate):
        return menu_crud.update_menu(self.db, menu_id, menu)

    def update_submenu(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        submenu: submenu_schema.SubmenuUpdate,
    ):
        return submenu_crud.update_submenu(self.db, menu_id, submenu_id, submenu)

    def update_dish(
        self,
        submenu_id: UUID,
        dish_id: UUID,
        dish: dish_schema.DishUpdate,
    ):
        return dish_crud.update_dish(self.db, submenu_id, dish_id, dish)

    def delete_menu(self, menu_id: UUID):
        return menu_crud.delete_menu(self.db, menu_id)

    def delete_submenu(self, menu_id: UUID, submenu_id: UUID):
        return submenu_crud.delete_submenu(self.db, menu_id, submenu_id)

    def delete_dish(self, submenu_id: UUID, dish_id: UUID):
        return dish_crud.delete_dish(self.db, submenu_id, dish_id)
