import json
from typing import List
from uuid import UUID

from pydantic import parse_obj_as
from pydantic.json import pydantic_encoder

from .restaurant_repo import RestaurantRepository
from .schemas.dish import Dish as DishShema, DishCreate, DishUpdate
from .schemas.menu import Menu as MenuSchema, MenuCreate, MenuUpdate
from .schemas.submenu import Submenu as SubmenuSchema, SubmenuCreate, SubmenuUpdate

cache = dict()


def cached_read(key, schema_class, model_loader):
    if key not in cache:
        print(f'Cache miss. Key: {key}')

        data_for_dump = parse_obj_as(schema_class, model_loader())

        cache[key] = json.dumps(data_for_dump, default=pydantic_encoder)
    else:
        print(f'Cache hit. Key: {key}')

    loaded_data = json.loads(cache[key])

    return parse_obj_as(schema_class, loaded_data)


class RestaurantService:
    def __init__(self, repo: RestaurantRepository):
        self.repo = repo

    def read_menus(self):
        return cached_read('menus', List[MenuSchema], lambda: self.repo.read_menus())
    
    def read_menu(self, menu_id: UUID):
        cache_key = f'menus/{menu_id}'
        return cached_read(cache_key, MenuSchema, lambda: self.repo.read_menu(menu_id))

    def create_menu(self, menu: MenuCreate):
        cache.clear()
        return self.repo.create_menu(menu)
    
    def update_menu(self, menu_id: UUID, menu: MenuUpdate):
        cache.clear()
        return self.repo.update_menu(menu_id, menu)
    
    def delete_menu(self, menu_id: UUID):
        cache.clear()
        return self.repo.delete_menu(menu_id)
    
    def create_submenu(self, menu_id: UUID, submenu: SubmenuCreate):
        cache.clear()
        return self.repo.create_submenu(menu_id, submenu)

    def create_dish(self, submenu_id: UUID, dish: DishCreate):
        cache.clear()
        return self.repo.create_dish(submenu_id, dish)

    def update_submenu(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        submenu: SubmenuUpdate,
    ):
        cache.clear()
        return self.repo.update_submenu(menu_id, submenu_id, submenu)

    def update_dish(
        self,
        submenu_id: UUID,
        dish_id: UUID,
        dish: DishUpdate,
    ):
        cache.clear()
        return self.repo.update_dish(submenu_id, dish_id, dish)

    def delete_submenu(self, menu_id: UUID, submenu_id: UUID):
        cache.clear()
        return self.repo.delete_submenu(menu_id, submenu_id)

    def delete_dish(self, submenu_id: UUID, dish_id: UUID):
        cache.clear()
        return self.repo.delete_dish(submenu_id, dish_id)
