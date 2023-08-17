import os
from uuid import UUID

# import requests
from menu_app.database import engine
from sqlalchemy.sql import text

LOCAL_URL = os.getenv('LOCAL_URL')
menu_content_url = f'{LOCAL_URL}/api/v1/menu_content'


def insert_menu(id: int, title: str, description: str) -> None:
    engine.execute(
        text('INSERT INTO menus (id, title, description) VALUES (:id, :title, :description)'),
        {
            'id': int_to_uuid(id),
            'title': title,
            'description': description,
        }
    )


def insert_submenu(menu_id: int, id: int, title: str, description: str) -> None:
    engine.execute(
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


def insert_dish(submenu_id: int, id: int, title: str, description: str, price: float) -> None:
    engine.execute(
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


def int_to_uuid(num: int) -> UUID:
    return UUID(str(num).rjust(32, '0'))


def test_export() -> None:
    insert_menu(1, 'Меню', 'Основное меню')

    insert_submenu(1, 1, 'Холодные закуски', 'К пиву')
    insert_dish(1, 1, 'Сельдь Бисмарк', 'Традиционное немецкое блюдо из маринованной сельди', 182.99)  # noqa: E501
    insert_dish(1, 2, 'Мясная тарелка', 'Нарезка из ветчины, колбасных колечек, нескольких сортов сыра и фруктов', 215.36)  # noqa: E501

    insert_submenu(1, 2, 'Рамен', 'Горячий рамен')
    insert_dish(2, 3, 'Дайзу рамен', 'Рамен на курином бульоне с куриными подушками и яйцом аджитама, яично-пшеничной лапшой, ростки зелени, грибами муэр и зеленым луком', 166.47)  # noqa: E501

    insert_menu(2, 'Алкогольное меню', 'Алкогольные напитки')

    insert_submenu(2, 3, 'Красные вина', 'Для романтичного вечера')
    insert_dish(3, 4, 'Шемен де Пап ля Ноблесс', 'Вино красное — фруктовое, среднетелое, выдержанное в дубе', 2700.79)  # noqa: E501

    # export_data = requests.get(menu_content_url).json()

    # assert export_data == "[[UUID('00000000-0000-0000-0000-000000000001'), 'Меню', 'Основное меню', ' ', ' ', ' '], [' ', UUID('00000000-0000-0000-0000-000000000001'), 'Холодные закуски', 'К пиву', ' ', ' '], [' ', ' ', UUID('00000000-0000-0000-0000-000000000001'), 'Сельдь Бисмарк', 'Традиционное немецкое блюдо из маринованной сельди', Decimal('182.99')], [' ', ' ', UUID('00000000-0000-0000-0000-000000000002'), 'Мясная тарелка', 'Нарезка из ветчины, колбасных колечек, нескольких сортов сыра и фруктов', Decimal('215.36')], [' ', UUID('00000000-0000-0000-0000-000000000002'), 'Рамен', 'Горячий рамен', ' ', ' '], [' ', ' ', UUID('00000000-0000-0000-0000-000000000003'), 'Дайзу рамен', 'Рамен на курином бульоне с куриными подушками и яйцом аджитама, яично-пшеничной лапшой, ростки зелени, грибами муэр и зеленым луком', Decimal('166.47')], [UUID('00000000-0000-0000-0000-000000000002'), 'Алкогольное меню', 'Алкогольные напитки', ' ', ' ', ' '], [' ', UUID('00000000-0000-0000-0000-000000000003'), 'Красные вина', 'Для романтичного вечера', ' ', ' '], [' ', ' ', UUID('00000000-0000-0000-0000-000000000004'), 'Шемен де Пап ля Ноблесс', 'Вино красное — фруктовое, среднетелое, выдержанное в дубе', Decimal('2700.79')]]"  # noqa: E501
