from uuid import UUID

from fastapi import Depends, FastAPI, status
from sqlalchemy.orm import Session

from .crud import dish as dish_crud
from .crud import menu as menu_crud
from .crud import submenu as submenu_crud
from .database import SessionLocal, engine
from .models import dish as dish_model
from .models import menu as menu_model
from .models import submenu as submenu_model
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


@app.get('/api/v1/menus')
def read_menus(db: Session = Depends(get_db)):
    return menu_crud.read_menus(db)


@app.get('/api/v1/menus/{menu_id}/submenus')
def read_submenus(menu_id: UUID, db: Session = Depends(get_db)):
    return submenu_crud.read_submenus(db, menu_id)


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
def read_dishes(submenu_id: UUID, db: Session = Depends(get_db)):
    return dish_crud.read_dishes(db, submenu_id)


@app.get('/api/v1/menus/{menu_id}')
def read_menu(menu_id: UUID, db: Session = Depends(get_db)):
    return menu_crud.read_menu(db, menu_id)


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
def read_submenu(
    menu_id: UUID,
    submenu_id: UUID,
    db: Session = Depends(get_db)
):
    return submenu_crud.read_submenu(db, menu_id, submenu_id)


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
def read_dish(submenu_id: UUID, dish_id: UUID, db: Session = Depends(get_db)):
    return dish_crud.read_dish(db, submenu_id, dish_id)


@app.post('/api/v1/menus', status_code=status.HTTP_201_CREATED)
def create_menu(menu: menu_schema.MenuCreate, db: Session = Depends(get_db)):
    return menu_crud.create_menu(db, menu)


@app.post(
    '/api/v1/menus/{menu_id}/submenus',
    status_code=status.HTTP_201_CREATED,
)
def create_submenu(
    submenu: submenu_schema.SubmenuCreate,
    menu_id: UUID,
    db: Session = Depends(get_db),
):
    return submenu_crud.create_submenu(db, menu_id, submenu)


@app.post(
    '/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
    status_code=status.HTTP_201_CREATED,
)
def create_dish(
    dish: dish_schema.DishCreate,
    submenu_id: UUID,
    db: Session = Depends(get_db)
):
    return dish_crud.create_dish(db, submenu_id, dish)


@app.patch('/api/v1/menus/{menu_id}')
def update_menu(
    menu: menu_schema.MenuUpdate,
    menu_id: UUID,
    db: Session = Depends(get_db,),
):
    return menu_crud.update_menu(db, menu_id, menu)


@app.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
def update_submenu(
    submenu: submenu_schema.SubmenuUpdate,
    menu_id: UUID,
    submenu_id: UUID,
    db: Session = Depends(get_db),
):
    return submenu_crud.update_submenu(db, menu_id, submenu_id, submenu)


@app.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
def update_dish(
    dish: dish_schema.DishUpdate,
    submenu_id: UUID,
    dish_id: UUID,
    db: Session = Depends(get_db),
):
    return dish_crud.update_dish(db, submenu_id, dish_id, dish)


@app.delete('/api/v1/menus/{menu_id}')
def delete_menu(menu_id: UUID, db: Session = Depends(get_db)):
    return menu_crud.delete_menu(db, menu_id)


@app.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
def delete_submenu(menu_id: UUID, submenu_id, db: Session = Depends(get_db)):
    return submenu_crud.delete_submenu(db, menu_id, submenu_id)


@app.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
def delete_dish(
    submenu_id: UUID,
    dish_id: UUID,
    db: Session = Depends(get_db),
):
    return dish_crud.delete_dish(db, submenu_id, dish_id)
