from uuid import UUID

from pydantic import parse_obj_as

from .models.dish import Dish
from .models.menu import Menu
from .models.submenu import Submenu
from .redis_cache import RedisCache
from .restaurant_repo import RestaurantRepository
from .schemas.dish import Dish as DishSchema
from .schemas.dish import DishCreate, DishUpdate
from .schemas.menu import Menu as MenuSchema
from .schemas.menu import MenuCreate, MenuUpdate
from .schemas.submenu import Submenu as SubmenuSchema
from .schemas.submenu import SubmenuCreate, SubmenuUpdate


class RestaurantService:
    def __init__(self, repo: RestaurantRepository) -> None:
        self.repo = repo

    def read_menus(self) -> list[MenuSchema]:
        cache_key = get_menu_list_key()
        return RedisCache.read(cache_key, list[MenuSchema], lambda: self.repo.read_menus())

    def read_submenus(self, menu_id: UUID) -> list[SubmenuSchema]:
        cache_key = get_submenu_list_key(menu_id)
        return RedisCache.read(
            cache_key,
            list[SubmenuSchema],
            lambda: self.repo.read_submenus(menu_id),
        )

    def read_dishes(self, menu_id: UUID, submenu_id: UUID) -> list[DishSchema]:
        cache_key = get_dish_list_key(menu_id, submenu_id)
        return RedisCache.read(cache_key, list[DishSchema], lambda: self.repo.read_dishes(submenu_id))

    def read_menu(self, menu_id: UUID) -> MenuSchema:
        cache_key = get_menu_item_key(menu_id)
        return RedisCache.read(cache_key, MenuSchema, lambda: self.repo.read_menu(menu_id))

    def read_submenu(self, menu_id: UUID, submenu_id: UUID) -> SubmenuSchema:
        cache_key = get_submenu_item_key(menu_id, submenu_id)
        return RedisCache.read(
            cache_key,
            SubmenuSchema,
            lambda: self.repo.read_submenu(menu_id, submenu_id),
        )

    def read_dish(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID) -> DishSchema:
        cache_key = get_dish_item_key(menu_id, submenu_id, dish_id)
        return RedisCache.read(cache_key, DishSchema, lambda: self.repo.read_dish(submenu_id, dish_id))

    def create_menu(self, menu: MenuCreate) -> MenuSchema:
        invalidate_menu_list()

        menu_model = Menu(title=menu.title, description=menu.description)
        menu_model = self.repo.save_menu(menu_model, True)

        return parse_obj_as(MenuSchema, menu_model)

    def update_menu(self, menu_id: UUID, menu_update: MenuUpdate) -> MenuSchema:
        invalidate_menu_item(menu_id)

        menu_model = self.repo.read_menu(menu_id)
        menu_model.title = menu_update.title
        menu_model.description = menu_update.description
        menu_model = self.repo.save_menu(menu_model, False)

        return parse_obj_as(MenuSchema, menu_model)

    def delete_menu(self, menu_id: UUID) -> dict[str, bool]:
        invalidate_menu_item(menu_id)
        return self.repo.delete_menu(menu_id)

    def create_submenu(self, menu_id: UUID, submenu: SubmenuCreate) -> SubmenuSchema:
        invalidate_submenu_list(menu_id)

        submenu_model = Submenu(
            menu_id=menu_id,
            title=submenu.title,
            description=submenu.description,
        )
        submenu_model = self.repo.save_submenu(submenu_model, True)

        return parse_obj_as(SubmenuSchema, submenu_model)

    def create_dish(self, menu_id: UUID, submenu_id: UUID, dish: DishCreate) -> DishSchema:
        invalidate_dish_list(menu_id, submenu_id)

        dish_model = Dish(
            title=dish.title,
            description=dish.description,
            price=dish.price,
            submenu_id=submenu_id,
        )

        dish_model = self.repo.save_dish(dish_model, True)

        return parse_obj_as(DishSchema, dish_model)

    def update_submenu(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        submenu_update: SubmenuUpdate,
    ) -> SubmenuSchema:
        invalidate_submenu_item(menu_id, submenu_id)

        submenu_model = self.repo.read_submenu(menu_id, submenu_id)
        submenu_model.title = submenu_update.title
        submenu_model.description = submenu_update.description
        submenu_model = self.repo.save_submenu(submenu_model, False)

        return parse_obj_as(SubmenuSchema, submenu_model)

    def update_dish(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        dish_id: UUID,
        dish_update: DishUpdate,
    ) -> DishSchema:
        invalidate_dish_item(menu_id, submenu_id, dish_id)

        dish_model = self.repo.read_dish(submenu_id, dish_id)
        dish_model.title = dish_update.title
        dish_model.description = dish_update.description
        dish_model.price = dish_update.price
        dish_model = self.repo.save_dish(dish_model, False)

        return parse_obj_as(DishSchema, dish_model)

    def delete_submenu(self, menu_id: UUID, submenu_id: UUID) -> dict[str, bool]:
        invalidate_submenu_item(menu_id, submenu_id)
        return self.repo.delete_submenu(menu_id, submenu_id)

    def delete_dish(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID) -> dict[str, bool]:
        invalidate_dish_item(menu_id, submenu_id, dish_id)
        return self.repo.delete_dish(submenu_id, dish_id)


def get_menu_list_key() -> str:
    return 'menus'


def get_menu_item_key(menu_id: UUID) -> str:
    return f'{get_menu_list_key()}/{menu_id}'


def get_submenu_list_key(menu_id: UUID) -> str:
    return f'{get_menu_item_key(menu_id)}/submenus'


def get_submenu_item_key(menu_id: UUID, submenu_id: UUID) -> str:
    return f'{get_submenu_list_key(menu_id)}/{submenu_id}'


def get_dish_list_key(menu_id: UUID, submenu_id: UUID) -> str:
    return f'{get_submenu_item_key(menu_id, submenu_id)}/dishes'


def get_dish_item_key(menu_id: UUID, submenu_id: UUID, dish_id: UUID) -> str:
    return f'{get_dish_list_key(menu_id, submenu_id)}/{dish_id}'


# Clear funcs

def invalidate_menu_list() -> None:
    print('invalidate_menu_list')
    RedisCache.delete(get_menu_list_key())


def invalidate_submenu_list(menu_id: UUID) -> None:
    print('invalidate_submenu_list')
    RedisCache.delete(get_submenu_list_key(menu_id))
    invalidate_menu_item(menu_id)


def invalidate_dish_list(menu_id: UUID, submenu_id: UUID) -> None:
    print('invalidate_dish_list')
    RedisCache.delete(get_dish_list_key(menu_id, submenu_id))
    invalidate_submenu_item(menu_id, submenu_id)


def invalidate_menu_item(menu_id: UUID) -> None:
    print('invalidate_menu_item')
    RedisCache.delete(get_menu_item_key(menu_id))
    invalidate_menu_list()


def invalidate_submenu_item(menu_id: UUID, submenu_id: UUID) -> None:
    print('invalidate_submenu_item')
    RedisCache.delete(get_submenu_item_key(menu_id, submenu_id))
    invalidate_submenu_list(menu_id)


def invalidate_dish_item(menu_id: UUID, submenu_id: UUID, dish_id: UUID) -> None:
    print('invalidate_dish_item')
    RedisCache.delete(get_dish_item_key(menu_id, submenu_id, dish_id))
    invalidate_dish_list(menu_id, submenu_id)
