from uuid import UUID

from fastapi import Depends, FastAPI, status
from sqlalchemy.orm import Session

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
def read_submenus(menu_id: UUID, svc: RestaurantService = Depends(get_service)) -> list[submenu_schema.Submenu]:
    return svc.read_submenus(menu_id)


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
def read_dishes(menu_id: UUID, submenu_id: UUID, svc: RestaurantService = Depends(get_service)) -> list[dish_schema.Dish]:
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
def read_dish(menu_id: UUID, submenu_id: UUID, dish_id: UUID, svc: RestaurantService = Depends(get_service)) -> dish_schema.Dish:
    return svc.read_dish(menu_id, submenu_id, dish_id)


@app.post('/api/v1/menus', status_code=status.HTTP_201_CREATED)
def create_menu(menu: menu_schema.MenuCreate, svc: RestaurantService = Depends(get_service)) -> menu_schema.Menu:
    return svc.create_menu(menu)


@app.post(
    '/api/v1/menus/{menu_id}/submenus',
    status_code=status.HTTP_201_CREATED,
)
def create_submenu(
    submenu: submenu_schema.SubmenuCreate,
    menu_id: UUID,
    svc: RestaurantService = Depends(get_service),
) -> submenu_schema.Submenu:
    return svc.create_submenu(menu_id, submenu)


@app.post(
    '/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
    status_code=status.HTTP_201_CREATED,
)
def create_dish(
    menu_id: UUID,
    submenu_id: UUID,
    dish: dish_schema.DishCreate,
    svc: RestaurantService = Depends(get_service),
) -> dish_schema.Dish:
    return svc.create_dish(menu_id, submenu_id, dish)


@app.patch('/api/v1/menus/{menu_id}')
def update_menu(
    menu_id: UUID,
    menu_update: menu_schema.MenuUpdate,
    svc: RestaurantService = Depends(get_service),
) -> menu_schema.Menu:
    return svc.update_menu(menu_id, menu_update)


@app.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
def update_submenu(
    menu_id: UUID,
    submenu_id: UUID,
    submenu_update: submenu_schema.SubmenuUpdate,
    svc: RestaurantService = Depends(get_service),
) -> submenu_schema.Submenu:
    return svc.update_submenu(menu_id, submenu_id, submenu_update)


@app.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
def update_dish(
    menu_id: UUID,
    submenu_id: UUID,
    dish_id: UUID,
    dish_update: dish_schema.DishUpdate,
    svc: RestaurantService = Depends(get_service),
) -> dish_schema.Dish:
    return svc.update_dish(menu_id, submenu_id, dish_id, dish_update)


@app.delete('/api/v1/menus/{menu_id}')
def delete_menu(menu_id: UUID, svc: RestaurantService = Depends(get_service)) -> dict[str, bool]:
    return svc.delete_menu(menu_id)


@app.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
def delete_submenu(menu_id: UUID, submenu_id: UUID, svc: RestaurantService = Depends(get_service)) -> dict[str, bool]:
    return svc.delete_submenu(menu_id, submenu_id)


@app.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
def delete_dish(
    menu_id: UUID,
    submenu_id: UUID,
    dish_id: UUID,
    svc: RestaurantService = Depends(get_service),
) -> dict[str, bool]:
    return svc.delete_dish(menu_id, submenu_id, dish_id)


@app.get('/api/v1/menu_content')
def export(db: Session = Depends(get_db)):  # TODO: add output type
    from sqlalchemy.sql import text

    statement = text('SELECT * FROM menus JOIN submenus ON menus.id = submenus.menu_id JOIN dishes ON submenus.id = \
        dishes.submenu_id ORDER BY menus.id, submenus.id, dishes.id')
    return ' '.join([str(_) for _ in db.execute(statement)])
