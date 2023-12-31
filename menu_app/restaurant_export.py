from uuid import UUID

from menu_app.models.dish import Dish
from menu_app.models.menu import Menu
from menu_app.models.submenu import Submenu
from sqlalchemy import select
from sqlalchemy.engine.row import Row
from sqlalchemy.ext.asyncio import AsyncSession


def make_csv_text(lists_list: list[list]) -> str:
    rows: map[str] = map(
        lambda row: '\t'.join(map(str, row)),
        lists_list,
    )
    return '\n'.join(rows)


async def restaurant_menu_export(db: AsyncSession) -> str:
    result = await db.execute(
        select(
            Menu.id, Menu.title, Menu.description,
            Submenu.id, Submenu.title, Submenu.description,
            Dish.id, Dish.title, Dish.description, Dish.price,
        )
        .select_from(Menu)
        .join(Submenu)
        .join(Dish)
        .order_by(Menu.id, Submenu.id, Dish.id),
    )
    export_data: list[Row] = result.all()

    export_rows: list[list] = []
    current_menu_id: UUID | None = None
    current_submenu_id: UUID | None = None

    for export_row in export_data:
        menu_id, menu_title, menu_description, \
            submenu_id, submenu_title, submenu_description, \
            dish_id, dish_title, dish_description, dish_price = export_row

        if menu_id != current_menu_id:
            export_rows.append(
                [
                    menu_id,
                    menu_title,
                    menu_description,
                    '',
                    '',
                    '',
                ],
            )
            current_menu_id = menu_id

        if submenu_id != current_submenu_id:
            export_rows.append(
                [
                    '',
                    submenu_id,
                    submenu_title,
                    submenu_description,
                    '',
                    '',
                ],
            )
            current_submenu_id = submenu_id

        export_rows.append(
            [
                '',
                '',
                dish_id,
                dish_title,
                dish_description,
                dish_price,
            ],
        )

    return make_csv_text(export_rows)
