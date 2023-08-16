import os
from uuid import UUID

import requests
from menu_app.database import engine
from sqlalchemy.sql import text

LOCAL_URL = os.getenv('LOCAL_URL')
menu_content_url = f'{LOCAL_URL}/api/v1/menu_content'


def int_to_uuid(num):
    return UUID(str(num).rjust(32, '0'))


def test_export() -> None:
    engine.execute(
        text('INSERT INTO menus (id, title, description) VALUES (:id, :title, :description)'),
        {
            'id': int_to_uuid(1),
            'title': 'Меню',
            'description': 'Основное меню',
        }
    )

    engine.execute(
        text('INSERT INTO submenus (menu_id, id, title, description) VALUES (:menu_id, :id, :title, :description)'),
        {
            'menu_id': int_to_uuid(1),
            'id': int_to_uuid(1),
            'title': 'Холодные закуски',
            'description': 'К пиву',
        }
    )

    engine.execute(
        text('INSERT INTO dishes (submenu_id, id, title, description, price) VALUES (:submenu_id, :id, :title, \
            :description, :price)'),
        {
            'submenu_id': int_to_uuid(1),
            'id': int_to_uuid(1),
            'title': 'Сельдь Бисмарк',
            'description': 'Традиционное немецкое блюдо из маринованной сельди',
            'price': 182.99,
        }
    )

    engine.execute(
        text('INSERT INTO dishes (submenu_id, id, title, description, price) VALUES (:submenu_id, :id, :title, \
            :description, :price)'),
        {
            'submenu_id': int_to_uuid(1),
            'id': int_to_uuid(2),
            'title': 'Мясная тарелка',
            'description': 'Нарезка из ветчины, колбасных колечек, нескольких сортов сыра и фруктов',
            'price': 215.36,
        }
    )

    engine.execute(
        text('INSERT INTO submenus (menu_id, id, title, description) VALUES (:menu_id, :id, :title, :description)'),
        {
            'menu_id': int_to_uuid(1),
            'id': int_to_uuid(2),
            'title': 'Рамен',
            'description': 'Горячий рамен',
        }
    )

    engine.execute(
        text('INSERT INTO dishes (submenu_id, id, title, description, price) VALUES (:submenu_id, :id, :title, \
            :description, :price)'),
        {
            'submenu_id': int_to_uuid(2),
            'id': int_to_uuid(3),
            'title': 'Дайзу рамен',
            'description': 'Рамен на курином бульоне с куриными подушками и яйцом аджитама, яично-пшеничной лапшой, ростки зелени, грибами муэр и зеленым луком',  # noqa: E501
            'price': 166.47,
        }
    )

    engine.execute(
        text('INSERT INTO dishes (submenu_id, id, title, description, price) VALUES (:submenu_id, :id, :title, \
            :description, :price)'),
        {
            'submenu_id': int_to_uuid(2),
            'id': int_to_uuid(4),
            'title': 'Унаги рамен',
            'description': 'Рамен на нежном сливочном рыбном бульоне, с добавлением маринованного угря, грибов муэр, кунжута, зеленого лука',  # noqa: E501
            'price': 168.25,
        }
    )

    engine.execute(
        text('INSERT INTO menus (id, title, description) VALUES (:id, :title, :description)'),
        {
            'id': int_to_uuid(2),
            'title': 'Алкогольное меню',
            'description': 'Алкогольные напитки',
        }
    )

    engine.execute(
        text('INSERT INTO submenus (menu_id, id, title, description) VALUES (:menu_id, :id, :title, :description)'),
        {
            'menu_id': int_to_uuid(2),
            'id': int_to_uuid(3),
            'title': 'Красные вина',
            'description': 'Для романтичного вечера',
        }
    )

    engine.execute(
        text('INSERT INTO dishes (submenu_id, id, title, description, price) VALUES (:submenu_id, :id, :title, \
            :description, :price)'),
        {
            'submenu_id': int_to_uuid(3),
            'id': int_to_uuid(5),
            'title': 'Шемен де Пап ля Ноблесс',
            'description': 'Вино красное — фруктовое, среднетелое, выдержанное в дубе',
            'price': 2700.79,
        }
    )

    engine.execute(
        text('INSERT INTO dishes (submenu_id, id, title, description, price) VALUES (:submenu_id, :id, :title, \
            :description, :price)'),
        {
            'submenu_id': int_to_uuid(3),
            'id': int_to_uuid(6),
            'title': 'Рипароссо Монтепульчано',
            'description': 'Вино красное, сухое',
            'price': 3100.33,
        }
    )

    engine.execute(
        text('INSERT INTO submenus (menu_id, id, title, description) VALUES (:menu_id, :id, :title, :description)'),
        {
            'menu_id': int_to_uuid(2),
            'id': int_to_uuid(4),
            'title': 'Виски',
            'description': 'Для интересных бесед',
        }
    )

    engine.execute(
        text('INSERT INTO dishes (submenu_id, id, title, description, price) VALUES (:submenu_id, :id, :title, \
            :description, :price)'),
        {
            'submenu_id': int_to_uuid(4),
            'id': int_to_uuid(7),
            'title': 'Джемисон',
            'description': 'Классический купажированный виски, проходящий 4-хлетнюю выдержку в дубовых бочках',
            'price': 420.78,
        }
    )

    engine.execute(
        text('INSERT INTO dishes (submenu_id, id, title, description, price) VALUES (:submenu_id, :id, :title, \
            :description, :price)'),
        {
            'submenu_id': int_to_uuid(4),
            'id': int_to_uuid(8),
            'title': 'Джек Дэниелс',
            'description': 'Характерен мягкий вкус, сочетает в себе карамельно-ванильные и древесные нотки. Легкий привкус дыма.',  # noqa: E501
            'price': 440.11,
        }
    )

    export_data = requests.get(menu_content_url).json()

    assert export_data == "(UUID('00000000-0000-0000-0000-000000000001'), 'Меню', 'Основное меню', UUID('00000000-0000-0000-0000-000000000001'), 'Холодные закуски', 'К пиву', UUID('00000000-0000-0000-0000-000000000001'), UUID('00000000-0000-0000-0000-000000000001'), 'Сельдь Бисмарк', 'Традиционное немецкое блюдо из маринованной сельди', Decimal('182.99'), UUID('00000000-0000-0000-0000-000000000001')) (UUID('00000000-0000-0000-0000-000000000001'), 'Меню', 'Основное меню', UUID('00000000-0000-0000-0000-000000000001'), 'Холодные закуски', 'К пиву', UUID('00000000-0000-0000-0000-000000000001'), UUID('00000000-0000-0000-0000-000000000002'), 'Мясная тарелка', 'Нарезка из ветчины, колбасных колечек, нескольких сортов сыра и фруктов', Decimal('215.36'), UUID('00000000-0000-0000-0000-000000000001')) (UUID('00000000-0000-0000-0000-000000000001'), 'Меню', 'Основное меню', UUID('00000000-0000-0000-0000-000000000002'), 'Рамен', 'Горячий рамен', UUID('00000000-0000-0000-0000-000000000001'), UUID('00000000-0000-0000-0000-000000000003'), 'Дайзу рамен', 'Рамен на курином бульоне с куриными подушками и яйцом аджитама, яично-пшеничной лапшой, ростки зелени, грибами муэр и зеленым луком', Decimal('166.47'), UUID('00000000-0000-0000-0000-000000000002')) (UUID('00000000-0000-0000-0000-000000000001'), 'Меню', 'Основное меню', UUID('00000000-0000-0000-0000-000000000002'), 'Рамен', 'Горячий рамен', UUID('00000000-0000-0000-0000-000000000001'), UUID('00000000-0000-0000-0000-000000000004'), 'Унаги рамен', 'Рамен на нежном сливочном рыбном бульоне, с добавлением маринованного угря, грибов муэр, кунжута, зеленого лука', Decimal('168.25'), UUID('00000000-0000-0000-0000-000000000002')) (UUID('00000000-0000-0000-0000-000000000002'), 'Алкогольное меню', 'Алкогольные напитки', UUID('00000000-0000-0000-0000-000000000003'), 'Красные вина', 'Для романтичного вечера', UUID('00000000-0000-0000-0000-000000000002'), UUID('00000000-0000-0000-0000-000000000005'), 'Шемен де Пап ля Ноблесс', 'Вино красное — фруктовое, среднетелое, выдержанное в дубе', Decimal('2700.79'), UUID('00000000-0000-0000-0000-000000000003')) (UUID('00000000-0000-0000-0000-000000000002'), 'Алкогольное меню', 'Алкогольные напитки', UUID('00000000-0000-0000-0000-000000000003'), 'Красные вина', 'Для романтичного вечера', UUID('00000000-0000-0000-0000-000000000002'), UUID('00000000-0000-0000-0000-000000000006'), 'Рипароссо Монтепульчано', 'Вино красное, сухое', Decimal('3100.33'), UUID('00000000-0000-0000-0000-000000000003')) (UUID('00000000-0000-0000-0000-000000000002'), 'Алкогольное меню', 'Алкогольные напитки', UUID('00000000-0000-0000-0000-000000000004'), 'Виски', 'Для интересных бесед', UUID('00000000-0000-0000-0000-000000000002'), UUID('00000000-0000-0000-0000-000000000007'), 'Джемисон', 'Классический купажированный виски, проходящий 4-хлетнюю выдержку в дубовых бочках', Decimal('420.78'), UUID('00000000-0000-0000-0000-000000000004')) (UUID('00000000-0000-0000-0000-000000000002'), 'Алкогольное меню', 'Алкогольные напитки', UUID('00000000-0000-0000-0000-000000000004'), 'Виски', 'Для интересных бесед', UUID('00000000-0000-0000-0000-000000000002'), UUID('00000000-0000-0000-0000-000000000008'), 'Джек Дэниелс', 'Характерен мягкий вкус, сочетает в себе карамельно-ванильные и древесные нотки. Легкий привкус дыма.', Decimal('440.11'), UUID('00000000-0000-0000-0000-000000000004'))"  # noqa: E501
