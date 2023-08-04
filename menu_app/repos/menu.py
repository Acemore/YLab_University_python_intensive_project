from uuid import UUID

from sqlalchemy.orm import Session

from ..crud import menu as menu_crud
from ..schemas import menu as menu_schema


class MenuRepository(object):
    def __init__(self, db: Session):
        self.db = db

    def read_menus(self, db: Session):
        return menu_crud.read_menus(db)

    def read_menu(self, db: Session, menu_id: UUID):
        return menu_crud.read_menu(db, menu_id)

    def create_menu(self, db: Session, menu: menu_schema.MenuCreate):
        return menu_crud.create_menu(db, menu)

    def update_menu(self, db: Session, menu_id: UUID, menu: menu_schema.MenuUpdate):
        return menu_crud.update_menu(db, menu_id, menu)

    def delete_menu(self, db: Session, menu_id: UUID):
        return menu_crud.delete_menu(db, menu_id)
