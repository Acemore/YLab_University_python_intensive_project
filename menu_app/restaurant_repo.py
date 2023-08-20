from uuid import UUID

from menu_app.models.dish import Dish
from menu_app.models.menu import Menu
from menu_app.models.submenu import Submenu
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Этот файл работает только с моделями
# Не импортируй схемы сюда

# Используется общий репозиторий на все сущности,
# потому что они образуют общий агрегат:
#  - https://stackoverflow.com/a/2330912
#  - https://martinfowler.com/bliki/DDD_Aggregate.html


class RestaurantRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    # Menu

    async def read_menus(self) -> list[Menu]:
        result = await self.db.execute(select(Menu))
        return result.scalars().all()

    async def read_menu(self, menu_id: UUID) -> Menu:
        result = await self.db.execute(select(Menu).where(Menu.id == menu_id))
        return result.scalars().first()

    async def save_menu(self, menu: Menu, is_new: bool) -> Menu:
        if is_new:
            self.db.add(menu)

        await self.db.commit()
        await self.db.refresh(menu)

        return menu

    async def delete_menu(self, menu_id: UUID) -> None:
        result = await self.db.execute(select(Menu).where(Menu.id == menu_id))
        menu = result.scalars().first()

        await self.db.delete(menu)
        await self.db.commit()

        return None

    # Submenu

    async def read_submenus(self, menu_id: UUID) -> list[Submenu]:
        result = await self.db.execute(select(Submenu).where(Menu.id == menu_id))
        return result.scalars().all()

    async def read_submenu(self, menu_id: UUID, submenu_id: UUID) -> Submenu:
        result = await self.db.execute(
            select(Submenu).
            where(Menu.id == menu_id, Submenu.id == submenu_id),
        )
        return result.scalars().first()

    async def save_submenu(self, submenu: Submenu, is_new: bool) -> Submenu:
        if is_new:
            self.db.add(submenu)

        await self.db.commit()
        await self.db.refresh(submenu)

        return submenu

    async def delete_submenu(
        self,
        menu_id: UUID,
        submenu_id: UUID,
    ) -> None:
        result = await self.db.execute(
            select(Submenu).
            where(Menu.id == menu_id, Submenu.id == submenu_id),
        )
        submenu = result.scalars().first()

        await self.db.delete(submenu)
        await self.db.commit()

        return None

    # Dish

    async def read_dishes(self, submenu_id: UUID) -> list[Dish]:
        result = await self.db.execute(
            select(Dish).
            where(Submenu.id == submenu_id),
        )
        return result.scalars().all()

    async def read_dish(self, submenu_id: UUID, dish_id: UUID) -> Dish:
        result = await self.db.execute(
            select(Dish).
            where(Submenu.id == submenu_id, Dish.id == dish_id),
        )
        return result.scalars().first()

    async def save_dish(self, dish: Dish, is_new: bool) -> Dish:
        if is_new:
            self.db.add(dish)

        await self.db.commit()
        await self.db.refresh(dish)

        return dish

    async def delete_dish(
        self,
        submenu_id: UUID,
        dish_id: UUID,
    ) -> None:
        result = await self.db.execute(
            select(Dish).
            where(Submenu.id == submenu_id, Dish.id == dish_id),
        )
        dish = result.scalars().first()

        await self.db.delete(dish)
        await self.db.commit()

        return None
