from uuid import UUID

from sqlalchemy.engine.row import Row
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sqlalchemy.sql.expression import TextClause


def make_csv_text(lists_list: list[list]) -> str:
    rows: map[str] = map(
        lambda row: '\t'.join(map(str, row)),
        lists_list,
    )
    return '\n'.join(rows)


def restaurant_menu_export(db: Session) -> str:
    statement: TextClause = text(
        'SELECT\
         menus.id, menus.title, menus.description,\
         submenus.id, submenus.title, submenus.description,\
         dishes.id, dishes.title, dishes.description, dishes.price\
         FROM menus\
         JOIN submenus\
         ON menus.id = submenus.menu_id\
         JOIN dishes\
         ON submenus.id = dishes.submenu_id\
         ORDER BY menus.id, submenus.id, dishes.id'
    )
    export_data: list[Row] = db.execute(statement).fetchall()

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
