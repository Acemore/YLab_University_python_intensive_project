import json
import os
from typing import Any
from uuid import UUID

from pydantic import parse_obj_as
from pydantic.json import pydantic_encoder
from redis import Redis

from .models.menu import Menu
from .models.submenu import Submenu
from .restaurant_repo import RestaurantRepository
from .schemas.dish import Dish as DishSchema
from .schemas.dish import DishCreate, DishUpdate
from .schemas.menu import Menu as MenuSchema
from .schemas.menu import MenuCreate, MenuUpdate
from .schemas.submenu import Submenu as SubmenuSchema
from .schemas.submenu import SubmenuCreate, SubmenuUpdate

REDIS_HOST: str = str(os.getenv('REDIS_HOST'))
redis: Redis = Redis(host=REDIS_HOST, port=6379, db=0, decode_responses=True)


def cached_read(key, schema_class, model_loader) -> Any:
    if not redis.exists(key):
        print(f'Cache miss. Key: {key}')

        data_for_dump = parse_obj_as(schema_class, model_loader())

        redis.set(key, json.dumps(data_for_dump, default=pydantic_encoder))
    else:
        print(f'Cache hit. Key: {key}')

    loaded_data = json.loads(str(redis.get(key)))

    return parse_obj_as(schema_class, loaded_data)


def cache_clear() -> None:
    print('Clear cache')
    redis.flushdb()


class RestaurantService:
    def __init__(self, repo: RestaurantRepository) -> None:
        self.repo = repo

    def read_menus(self) -> list[MenuSchema]:
        return cached_read('menus', list[MenuSchema], lambda: self.repo.read_menus())

    def read_submenus(self, menu_id: UUID) -> list[SubmenuSchema]:
        return cached_read(
            'submenus',
            list[SubmenuSchema],
            lambda: self.repo.read_submenus(menu_id),
        )

    def read_dishes(self, submenu_id: UUID) -> list[DishSchema]:
        return cached_read('dishes', list[DishSchema], lambda: self.repo.read_dishes(submenu_id))

    def read_menu(self, menu_id: UUID) -> MenuSchema:
        cache_key = f'menus/{menu_id}'
        return cached_read(cache_key, MenuSchema, lambda: self.repo.read_menu(menu_id))

    def read_submenu(self, menu_id: UUID, submenu_id: UUID) -> SubmenuSchema:
        cache_key = f'submenus/{submenu_id}'
        return cached_read(
            cache_key,
            SubmenuSchema,
            lambda: self.repo.read_submenu(menu_id, submenu_id),
        )

    def read_dish(self, submenu_id: UUID, dish_id: UUID) -> DishSchema:
        cache_key = f'dishes/{dish_id}'
        return cached_read(cache_key, DishSchema, lambda: self.repo.read_dish(submenu_id, dish_id))

    def create_menu(self, menu: MenuCreate) -> MenuSchema:
        cache_clear()

        menu_model = Menu(title=menu.title, description=menu.description)

        return self.repo.save_menu(menu_model, True)

    def update_menu(self, menu_id: UUID, menu_update: MenuUpdate) -> MenuSchema:
        cache_clear()

        menu_model = self.repo.read_menu(menu_id)
        menu_model.title = menu_update.title
        menu_model.description = menu_update.description

        return self.repo.save_menu(menu_model, False)

    def delete_menu(self, menu_id: UUID) -> dict[str, bool]:
        cache_clear()
        return self.repo.delete_menu(menu_id)

    def create_submenu(self, menu_id: UUID, submenu: SubmenuCreate) -> SubmenuSchema:
        cache_clear()

        submenu_model = Submenu(
            menu_id=menu_id,
            title=submenu.title,
            description=submenu.description,
        )

        return self.repo.save_submenu(submenu_model, True)

    def create_dish(self, submenu_id: UUID, dish: DishCreate) -> DishSchema:
        cache_clear()
        return self.repo.create_dish(submenu_id, dish)

    def update_submenu(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        submenu_update: SubmenuUpdate,
    ) -> SubmenuSchema:
        cache_clear()

        submenu_model = self.repo.read_submenu(menu_id, submenu_id)

        submenu_model.title = submenu_update.title
        submenu_model.description = submenu_update.description

        return self.repo.save_submenu(submenu_model, False)

    def update_dish(
        self,
        submenu_id: UUID,
        dish_id: UUID,
        dish: DishUpdate,
    ) -> DishSchema:
        cache_clear()
        return self.repo.update_dish(submenu_id, dish_id, dish)

    def delete_submenu(self, menu_id: UUID, submenu_id: UUID) -> dict[str, bool]:
        cache_clear()
        return self.repo.delete_submenu(menu_id, submenu_id)

    def delete_dish(self, submenu_id: UUID, dish_id: UUID) -> dict[str, bool]:
        cache_clear()
        return self.repo.delete_dish(submenu_id, dish_id)
