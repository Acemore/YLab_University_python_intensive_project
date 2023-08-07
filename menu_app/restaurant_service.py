import json
import os
from uuid import UUID

from pydantic import parse_obj_as
from pydantic.json import pydantic_encoder
from redis import Redis

from .models.menu import Menu
from .restaurant_repo import RestaurantRepository
from .schemas.dish import Dish as DishShema
from .schemas.dish import DishCreate, DishUpdate
from .schemas.menu import Menu as MenuSchema
from .schemas.menu import MenuCreate, MenuUpdate
from .schemas.submenu import Submenu as SubmenuSchema
from .schemas.submenu import SubmenuCreate, SubmenuUpdate

REDIS_HOST: str = str(os.getenv('REDIS_HOST'))
redis: Redis = Redis(host=REDIS_HOST, port=6379, db=0, decode_responses=True)


def cached_read(key, schema_class, model_loader):
    if not redis.exists(key):
        print(f'Cache miss. Key: {key}')

        data_for_dump = parse_obj_as(schema_class, model_loader())

        redis.set(key, json.dumps(data_for_dump, default=pydantic_encoder))
    else:
        print(f'Cache hit. Key: {key}')

    loaded_data = json.loads(redis.get(key))

    return parse_obj_as(schema_class, loaded_data)


def cache_clear():
    print('Clear cache')
    redis.flushdb()


class RestaurantService:
    def __init__(self, repo: RestaurantRepository):
        self.repo = repo

    def read_menus(self):
        return cached_read('menus', list[MenuSchema], lambda: self.repo.read_menus())

    def read_submenus(self, menu_id: UUID):
        return cached_read(
            'submenus',
            list[SubmenuSchema],
            lambda: self.repo.read_submenus(menu_id),
        )

    def read_dishes(self, submenu_id: UUID):
        return cached_read('dishes', list[DishShema], lambda: self.repo.read_dishes(submenu_id))

    def read_menu(self, menu_id: UUID):
        cache_key = f'menus/{menu_id}'
        return cached_read(cache_key, MenuSchema, lambda: self.repo.read_menu(menu_id))

    def read_submenu(self, menu_id: UUID, submenu_id: UUID):
        cache_key = f'submenus/{submenu_id}'
        return cached_read(
            cache_key,
            SubmenuSchema,
            lambda: self.repo.read_submenu(menu_id, submenu_id),
        )

    def read_dish(self, submenu_id: UUID, dish_id: UUID):
        cache_key = f'dishes/{dish_id}'
        return cached_read(cache_key, DishShema, lambda: self.repo.read_dish(submenu_id, dish_id))

    def create_menu(self, menu: MenuCreate):
        cache_clear()

        menu_model = Menu(title=menu.title, description=menu.description)

        return self.repo.save_menu(menu_model, True)

    def update_menu(self, menu_id: UUID, menu_update: MenuUpdate):
        cache_clear()

        menu_model = self.repo.read_menu(menu_id)
        menu_model.title = menu_update.title
        menu_model.description = menu_update.description

        return self.repo.save_menu(menu_model, False)

    def delete_menu(self, menu_id: UUID):
        cache_clear()
        return self.repo.delete_menu(menu_id)

    def create_submenu(self, menu_id: UUID, submenu: SubmenuCreate):
        cache_clear()
        return self.repo.create_submenu(menu_id, submenu)

    def create_dish(self, submenu_id: UUID, dish: DishCreate):
        cache_clear()
        return self.repo.create_dish(submenu_id, dish)

    def update_submenu(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        submenu: SubmenuUpdate,
    ):
        cache_clear()
        return self.repo.update_submenu(menu_id, submenu_id, submenu)

    def update_dish(
        self,
        submenu_id: UUID,
        dish_id: UUID,
        dish: DishUpdate,
    ):
        cache_clear()
        return self.repo.update_dish(submenu_id, dish_id, dish)

    def delete_submenu(self, menu_id: UUID, submenu_id: UUID):
        cache_clear()
        return self.repo.delete_submenu(menu_id, submenu_id)

    def delete_dish(self, submenu_id: UUID, dish_id: UUID):
        cache_clear()
        return self.repo.delete_dish(submenu_id, dish_id)
