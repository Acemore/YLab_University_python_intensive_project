import os
from uuid import UUID

import pytest
import requests
from menu_app.database import async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

LOCAL_URL = os.getenv('LOCAL_URL')
menu_content_url = f'{LOCAL_URL}/api/v1/export'


def int_to_uuid(num: int) -> UUID:
    return UUID(str(num).rjust(32, '0'))


class TestExport:
    db: AsyncSession = async_session()

    async def insert_menu(self, id: int, title: str, description: str) -> None:
        await self.db.execute(
            text('INSERT INTO menus (id, title, description) VALUES (:id, :title, :description)'),
            {
                'id': int_to_uuid(id),
                'title': title,
                'description': description,
            }
        )

    async def insert_submenu(self, menu_id: int, id: int, title: str, description: str) -> None:
        await self.db.execute(
            text(
                'INSERT INTO submenus\
                (menu_id, id, title, description)\
                VALUES (:menu_id, :id, :title, :description)'
            ),
            {
                'menu_id': int_to_uuid(menu_id),
                'id': int_to_uuid(id),
                'title': title,
                'description': description,
            }
        )

    async def insert_dish(self, submenu_id: int, id: int, title: str, description: str, price: float) -> None:
        await self.db.execute(
            text(
                'INSERT INTO dishes\
                (submenu_id, id, title, description, price)\
                VALUES (:submenu_id, :id, :title, :description, :price)'
            ),
            {
                'submenu_id': int_to_uuid(submenu_id),
                'id': int_to_uuid(id),
                'title': title,
                'description': description,
                'price': price,
            }
        )

    async def clear_menu(self) -> None:
        await self.db.execute(text('DELETE FROM menus'))
        await self.db.commit()

    @pytest.mark.asyncio
    async def test_export(self) -> None:
        await self.insert_menu(1, 'Меню', 'Основное меню')

        await self.insert_submenu(1, 1, 'Холодные закуски', 'К пиву')
        await self.insert_dish(1, 1, 'Сельдь Бисмарк', 'Традиционное немецкое блюдо из маринованной сельди', 182.99)
        await self.insert_dish(1, 2, 'Мясная тарелка', 'Нарезка из ветчины, колбасных колечек, нескольких сортов сыра и фруктов', 215.36)

        await self.insert_submenu(1, 2, 'Рамен', 'Горячий рамен')
        await self.insert_dish(2, 3, 'Дайзу рамен', 'Рамен на курином бульоне с куриными подушками и яйцом аджитама, яично-пшеничной лапшой, ростки зелени, грибами муэр и зеленым луком', 166.47)

        await self.insert_menu(2, 'Алкогольное меню', 'Алкогольные напитки')

        await self.insert_submenu(2, 3, 'Красные вина', 'Для романтичного вечера')
        await self.insert_dish(3, 4, 'Шемен де Пап ля Ноблесс', 'Вино красное — фруктовое, среднетелое, выдержанное в дубе', 2700.79)

        await self.db.commit()

        export_data = requests.get(menu_content_url).text
        export_data = export_data.replace('\t', '|')

        export_rows = export_data.split('\n')

        assert export_rows[0] == '00000000-0000-0000-0000-000000000001|Меню|Основное меню|||'
        assert export_rows[1] == '|00000000-0000-0000-0000-000000000001|Холодные закуски|К пиву||'
        assert export_rows[2] == '||00000000-0000-0000-0000-000000000001|Сельдь Бисмарк|Традиционное немецкое блюдо из маринованной сельди|182.99'
        assert export_rows[3] == '||00000000-0000-0000-0000-000000000002|Мясная тарелка|Нарезка из ветчины, колбасных колечек, нескольких сортов сыра и фруктов|215.36'
        assert export_rows[4] == '|00000000-0000-0000-0000-000000000002|Рамен|Горячий рамен||'
        assert export_rows[5] == '||00000000-0000-0000-0000-000000000003|Дайзу рамен|Рамен на курином бульоне с куриными подушками и яйцом аджитама, яично-пшеничной лапшой, ростки зелени, грибами муэр и зеленым луком|166.47'
        assert export_rows[6] == '00000000-0000-0000-0000-000000000002|Алкогольное меню|Алкогольные напитки|||'
        assert export_rows[7] == '|00000000-0000-0000-0000-000000000003|Красные вина|Для романтичного вечера||'
        assert export_rows[8] == '||00000000-0000-0000-0000-000000000004|Шемен де Пап ля Ноблесс|Вино красное — фруктовое, среднетелое, выдержанное в дубе|2700.79'

        await self.clear_menu()
