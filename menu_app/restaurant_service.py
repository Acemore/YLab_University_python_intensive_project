from uuid import UUID

from fastapi import BackgroundTasks, HTTPException, status
from menu_app.models.dish import Dish
from menu_app.models.menu import Menu
from menu_app.models.submenu import Submenu
from menu_app.redis_cache import RedisCache
from menu_app.restaurant_repo import RestaurantRepository
from menu_app.schemas.dish import Dish as DishSchema
from menu_app.schemas.dish import DishCreate, DishUpdate
from menu_app.schemas.menu import Menu as MenuSchema
from menu_app.schemas.menu import MenuCreate, MenuUpdate
from menu_app.schemas.submenu import Submenu as SubmenuSchema
from menu_app.schemas.submenu import SubmenuCreate, SubmenuUpdate
from pydantic import parse_obj_as


def make_not_found_error(model_name: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'{model_name} not found',
    )


class RestaurantService:
    def __init__(self, repo: RestaurantRepository, bg_tasks: BackgroundTasks) -> None:
        self.repo = repo
        self.bg_tasks = bg_tasks

    # Menu

    async def read_menus(self) -> list[MenuSchema]:
        cache_key = get_menu_list_key()
        return await RedisCache.read(
            cache_key,
            list[MenuSchema],
            lambda: self.repo.read_menus(),
        )

    async def read_menu(self, menu_id: UUID) -> MenuSchema:
        cache_key = get_menu_item_key(menu_id)

        result = await RedisCache.read(
            cache_key,
            MenuSchema,
            lambda: self.repo.read_menu(menu_id),
        )
        if not result:
            raise make_not_found_error('menu')

        return result

    async def create_menu(self, menu: MenuCreate) -> MenuSchema:
        self.bg_tasks.add_task(invalidate_menu_list)

        menu_model = Menu(title=menu.title, description=menu.description)
        menu_model = await self.repo.save_menu(menu_model, True)

        return parse_obj_as(MenuSchema, menu_model)

    async def update_menu(
        self,
        menu_id: UUID,
        menu_update: MenuUpdate,
    ) -> MenuSchema:
        self.bg_tasks.add_task(invalidate_menu_item, menu_id)

        menu_model = await self.repo.read_menu(menu_id)
        menu_model.title = menu_update.title
        menu_model.description = menu_update.description
        menu_model = await self.repo.save_menu(menu_model, False)

        return parse_obj_as(MenuSchema, menu_model)

    async def delete_menu(self, menu_id: UUID) -> dict[str, bool]:
        self.bg_tasks.add_task(invalidate_menu_item, menu_id)

        result = await self.repo.delete_menu(menu_id)

        if not result:
            raise make_not_found_error('menu')

        return {'ok': True}

    # Submenu

    async def read_submenus(self, menu_id: UUID) -> list[SubmenuSchema]:
        cache_key = get_submenu_list_key(menu_id)
        return await RedisCache.read(
            cache_key,
            list[SubmenuSchema],
            lambda: self.repo.read_submenus(menu_id),
        )

    async def read_submenu(
        self,
        menu_id: UUID,
        submenu_id: UUID,
    ) -> SubmenuSchema:
        cache_key = get_submenu_item_key(menu_id, submenu_id)

        result = await RedisCache.read(
            cache_key,
            SubmenuSchema,
            lambda: self.repo.read_submenu(menu_id, submenu_id),
        )
        if not result:
            raise make_not_found_error('submenu')

        return result

    async def create_submenu(
        self,
        menu_id: UUID,
        submenu: SubmenuCreate,
    ) -> SubmenuSchema:
        self.bg_tasks.add_task(invalidate_submenu_list, menu_id)

        submenu_model = Submenu(
            menu_id=menu_id,
            title=submenu.title,
            description=submenu.description,
        )
        submenu_model = await self.repo.save_submenu(submenu_model, True)

        return parse_obj_as(SubmenuSchema, submenu_model)

    async def update_submenu(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        submenu_update: SubmenuUpdate,
    ) -> SubmenuSchema:
        self.bg_tasks.add_task(invalidate_submenu_item, menu_id, submenu_id)

        submenu_model = await self.repo.read_submenu(menu_id, submenu_id)
        submenu_model.title = submenu_update.title
        submenu_model.description = submenu_update.description
        submenu_model = await self.repo.save_submenu(submenu_model, False)

        return parse_obj_as(SubmenuSchema, submenu_model)

    async def delete_submenu(
        self,
        menu_id: UUID,
        submenu_id: UUID,
    ) -> dict[str, bool]:
        self.bg_tasks.add_task(invalidate_submenu_item, menu_id, submenu_id)

        result = await self.repo.delete_submenu(menu_id, submenu_id)

        if not result:
            raise make_not_found_error('submenu')

        return {'ok': True}

    # Dish

    async def read_dishes(
        self,
        menu_id: UUID,
        submenu_id: UUID,
    ) -> list[DishSchema]:
        cache_key = get_dish_list_key(menu_id, submenu_id)
        return await RedisCache.read(
            cache_key,
            list[DishSchema],
            lambda: self.repo.read_dishes(submenu_id),
        )

    async def read_dish(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        dish_id: UUID,
    ) -> DishSchema:
        cache_key = get_dish_item_key(menu_id, submenu_id, dish_id)

        result = await RedisCache.read(
            cache_key,
            DishSchema,
            lambda: self.repo.read_dish(submenu_id, dish_id),
        )
        if not result:
            raise make_not_found_error('dish')

        return result

    async def create_dish(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        dish: DishCreate,
    ) -> DishSchema:
        self.bg_tasks.add_task(invalidate_dish_list, menu_id, submenu_id)

        dish_model = Dish(
            title=dish.title,
            description=dish.description,
            price=dish.price,
            submenu_id=submenu_id,
        )
        dish_model = await self.repo.save_dish(dish_model, True)

        return parse_obj_as(DishSchema, dish_model)

    async def update_dish(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        dish_id: UUID,
        dish_update: DishUpdate,
    ) -> DishSchema:
        self.bg_tasks.add_task(invalidate_dish_item, menu_id, submenu_id, dish_id)

        dish_model = await self.repo.read_dish(submenu_id, dish_id)
        dish_model.title = dish_update.title
        dish_model.description = dish_update.description
        dish_model.price = dish_update.price
        dish_model = await self.repo.save_dish(dish_model, False)

        return parse_obj_as(DishSchema, dish_model)

    async def delete_dish(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        dish_id: UUID,
    ) -> dict[str, bool]:
        self.bg_tasks.add_task(invalidate_dish_item, menu_id, submenu_id, dish_id)

        result = await self.repo.delete_dish(submenu_id, dish_id)

        if not result:
            raise make_not_found_error('dish')

        return {'ok': True}


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

async def invalidate_menu_list() -> None:
    print('invalidate_menu_list')
    await RedisCache.delete(get_menu_list_key())


async def invalidate_submenu_list(menu_id: UUID) -> None:
    print('invalidate_submenu_list')
    await RedisCache.delete(get_submenu_list_key(menu_id))
    await invalidate_menu_item(menu_id)


async def invalidate_dish_list(menu_id: UUID, submenu_id: UUID) -> None:
    print('invalidate_dish_list')
    await RedisCache.delete(get_dish_list_key(menu_id, submenu_id))
    await invalidate_submenu_item(menu_id, submenu_id)


async def invalidate_menu_item(menu_id: UUID) -> None:
    print('invalidate_menu_item')
    await RedisCache.delete(get_menu_item_key(menu_id))
    await invalidate_menu_list()


async def invalidate_submenu_item(menu_id: UUID, submenu_id: UUID) -> None:
    print('invalidate_submenu_item')
    await RedisCache.delete(get_submenu_item_key(menu_id, submenu_id))
    await invalidate_submenu_list(menu_id)


async def invalidate_dish_item(menu_id: UUID, submenu_id: UUID, dish_id: UUID) -> None:
    print('invalidate_dish_item')
    await RedisCache.delete(get_dish_item_key(menu_id, submenu_id, dish_id))
    await invalidate_dish_list(menu_id, submenu_id)
