from uuid import UUID

from fastapi import BackgroundTasks, Depends, FastAPI, status
from sqlalchemy.engine.row import Row
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sqlalchemy.sql.expression import TextClause

from .database import SessionLocal, engine
from .models import dish as dish_model
from .models import menu as menu_model
from .models import submenu as submenu_model
from .restaurant_repo import RestaurantRepository
from .restaurant_service import RestaurantService
from .schemas import dish as dish_schema
from .schemas import menu as menu_schema
from .schemas import submenu as submenu_schema

dish_model.Base.metadata.create_all(engine)
menu_model.Base.metadata.create_all(engine)
submenu_model.Base.metadata.create_all(engine)

app: FastAPI = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_repo(db: Session = Depends(get_db)) -> RestaurantRepository:
    return RestaurantRepository(db)


def get_service(repo: RestaurantRepository = Depends(get_repo)) -> RestaurantService:
    return RestaurantService(repo)


@app.get('/api/v1/menus')
def read_menus(svc: RestaurantService = Depends(get_service)) -> list[menu_schema.Menu]:
    return svc.read_menus()


@app.get('/api/v1/menus/{menu_id}/submenus')
def read_submenus(
    menu_id: UUID,
    svc: RestaurantService = Depends(get_service),
) -> list[submenu_schema.Submenu]:
    return svc.read_submenus(menu_id)


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
def read_dishes(
    menu_id: UUID,
    submenu_id: UUID,
    svc: RestaurantService = Depends(get_service),
) -> list[dish_schema.Dish]:
    return svc.read_dishes(menu_id, submenu_id)


@app.get('/api/v1/menus/{menu_id}')
def read_menu(menu_id: UUID, svc: RestaurantService = Depends(get_service)) -> menu_schema.Menu:
    return svc.read_menu(menu_id)


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
def read_submenu(
    menu_id: UUID,
    submenu_id: UUID,
    svc: RestaurantService = Depends(get_service),
) -> submenu_schema.Submenu:
    return svc.read_submenu(menu_id, submenu_id)


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
def read_dish(
    menu_id: UUID,
    submenu_id: UUID,
    dish_id: UUID,
    svc: RestaurantService = Depends(get_service),
) -> dish_schema.Dish:
    return svc.read_dish(menu_id, submenu_id, dish_id)


@app.post('/api/v1/menus', status_code=status.HTTP_201_CREATED)
def create_menu(
    menu: menu_schema.MenuCreate,
    bg_tasks: BackgroundTasks,
    svc: RestaurantService = Depends(get_service),
) -> menu_schema.Menu:
    return svc.create_menu(menu, bg_tasks)


@app.post(
    '/api/v1/menus/{menu_id}/submenus',
    status_code=status.HTTP_201_CREATED,
)
def create_submenu(
    submenu: submenu_schema.SubmenuCreate,
    menu_id: UUID,
    bg_tasks: BackgroundTasks,
    svc: RestaurantService = Depends(get_service),
) -> submenu_schema.Submenu:
    return svc.create_submenu(menu_id, submenu, bg_tasks)


@app.post(
    '/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
    status_code=status.HTTP_201_CREATED,
)
def create_dish(
    menu_id: UUID,
    submenu_id: UUID,
    dish: dish_schema.DishCreate,
    bg_tasks: BackgroundTasks,
    svc: RestaurantService = Depends(get_service),
) -> dish_schema.Dish:
    return svc.create_dish(menu_id, submenu_id, dish, bg_tasks)


@app.patch('/api/v1/menus/{menu_id}')
def update_menu(
    menu_id: UUID,
    menu_update: menu_schema.MenuUpdate,
    bg_tasks: BackgroundTasks,
    svc: RestaurantService = Depends(get_service),
) -> menu_schema.Menu:
    return svc.update_menu(menu_id, menu_update, bg_tasks)


@app.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
def update_submenu(
    menu_id: UUID,
    submenu_id: UUID,
    submenu_update: submenu_schema.SubmenuUpdate,
    bg_tasks: BackgroundTasks,
    svc: RestaurantService = Depends(get_service),
) -> submenu_schema.Submenu:
    return svc.update_submenu(menu_id, submenu_id, submenu_update, bg_tasks)


@app.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
def update_dish(
    menu_id: UUID,
    submenu_id: UUID,
    dish_id: UUID,
    dish_update: dish_schema.DishUpdate,
    bg_tasks: BackgroundTasks,
    svc: RestaurantService = Depends(get_service),
) -> dish_schema.Dish:
    return svc.update_dish(menu_id, submenu_id, dish_id, dish_update, bg_tasks)


@app.delete('/api/v1/menus/{menu_id}')
def delete_menu(
    menu_id: UUID,
    bg_tasks: BackgroundTasks,
    svc: RestaurantService = Depends(get_service),
) -> dict[str, bool]:
    return svc.delete_menu(menu_id, bg_tasks)


@app.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
def delete_submenu(
    menu_id: UUID,
    submenu_id: UUID,
    bg_tasks: BackgroundTasks,
    svc: RestaurantService = Depends(get_service),
) -> dict[str, bool]:
    return svc.delete_submenu(menu_id, submenu_id, bg_tasks)


@app.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
def delete_dish(
    menu_id: UUID,
    submenu_id: UUID,
    dish_id: UUID,
    bg_tasks: BackgroundTasks,
    svc: RestaurantService = Depends(get_service),
) -> dict[str, bool]:
    return svc.delete_dish(menu_id, submenu_id, dish_id, bg_tasks)


@app.get('/api/v1/export')
def export(db: Session = Depends(get_db)) -> str:
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

    return lists_list_to_csv(export_rows)


def lists_list_to_csv(lists_list: list[list]) -> str:
    rows: map[str] = map(
        lambda _list: '\t'.join(map(str, _list)),
        lists_list,
    )
    return '\n'.join(rows)
