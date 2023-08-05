from uuid import UUID

from fastapi import Depends, FastAPI, status
from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from .models import dish as dish_model
from .models import menu as menu_model
from .models import submenu as submenu_model
from .restaurant_repo import RestaurantRepository
from .schemas import dish as dish_schema
from .schemas import menu as menu_schema
from .schemas import submenu as submenu_schema

dish_model.Base.metadata.create_all(engine)
menu_model.Base.metadata.create_all(engine)
submenu_model.Base.metadata.create_all(engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_repo(db: Session = Depends(get_db)):
    return RestaurantRepository(db)


@app.get('/api/v1/menus')
def read_menus(repo: RestaurantRepository = Depends(get_repo)):
    return repo.read_menus()


@app.get('/api/v1/menus/{menu_id}/submenus')
def read_submenus(menu_id: UUID, repo: RestaurantRepository = Depends(get_repo)):
    return repo.read_submenus(menu_id)


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
def read_dishes(submenu_id: UUID, repo: RestaurantRepository = Depends(get_repo)):
    return repo.read_dishes(submenu_id)


@app.get('/api/v1/menus/{menu_id}')
def read_menu(menu_id: UUID, repo=Depends(get_repo)):
    return repo.read_menu(menu_id)


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
def read_submenu(
    menu_id: UUID,
    submenu_id: UUID,
    repo: RestaurantRepository = Depends(get_repo)
):
    return repo.read_submenu(menu_id, submenu_id)


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
def read_dish(submenu_id: UUID, dish_id: UUID, repo: RestaurantRepository = Depends(get_repo)):
    return repo.read_dish(submenu_id, dish_id)


@app.post('/api/v1/menus', status_code=status.HTTP_201_CREATED)
def create_menu(menu: menu_schema.MenuCreate, repo: RestaurantRepository = Depends(get_repo)):
    return repo.create_menu(menu)


@app.post(
    '/api/v1/menus/{menu_id}/submenus',
    status_code=status.HTTP_201_CREATED,
)
def create_submenu(
    submenu: submenu_schema.SubmenuCreate,
    menu_id: UUID,
    repo: RestaurantRepository = Depends(get_repo),
):
    return repo.create_submenu(menu_id, submenu)


@app.post(
    '/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
    status_code=status.HTTP_201_CREATED,
)
def create_dish(
    dish: dish_schema.DishCreate,
    submenu_id: UUID,
    repo: RestaurantRepository = Depends(get_repo)
):
    return repo.create_dish(submenu_id, dish)


@app.patch('/api/v1/menus/{menu_id}')
def update_menu(
    menu: menu_schema.MenuUpdate,
    menu_id: UUID,
    repo: RestaurantRepository = Depends(get_repo),
):
    return repo.update_menu(menu_id, menu)


@app.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
def update_submenu(
    submenu: submenu_schema.SubmenuUpdate,
    menu_id: UUID,
    submenu_id: UUID,
    repo: RestaurantRepository = Depends(get_repo),
):
    return repo.update_submenu(menu_id, submenu_id, submenu)


@app.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
def update_dish(
    dish: dish_schema.DishUpdate,
    submenu_id: UUID,
    dish_id: UUID,
    repo: RestaurantRepository = Depends(get_repo),
):
    return repo.update_dish(submenu_id, dish_id, dish)


@app.delete('/api/v1/menus/{menu_id}')
def delete_menu(menu_id: UUID, repo: RestaurantRepository = Depends(get_repo)):
    return repo.delete_menu(menu_id)


@app.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
def delete_submenu(menu_id: UUID, submenu_id, repo: RestaurantRepository = Depends(get_repo)):
    return repo.delete_submenu(menu_id, submenu_id)


@app.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
def delete_dish(
    submenu_id: UUID,
    dish_id: UUID,
    repo: RestaurantRepository = Depends(get_repo),
):
    return repo.delete_dish(submenu_id, dish_id)
