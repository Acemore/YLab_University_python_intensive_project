from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from ..models.menu import Menu
from ..schemas import menu as menu_schema


def read_menus(db: Session):
    return db.query(Menu).all()


def read_menu(db: Session, menu_id: UUID):
    db_menu = db.query(Menu).get(menu_id)

    if db_menu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="menu not found",
        )

    return db_menu


def create_menu(db: Session, menu: menu_schema.MenuCreate):
    db_menu = Menu(title=menu.title, description=menu.description)

    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)

    return db_menu


def update_menu(db: Session, menu_id: UUID, menu: menu_schema.MenuUpdate):
    db_menu = db.query(Menu).get(menu_id)

    if db_menu:
        menu_data = menu.dict()

        for key, value in menu_data.items():
            setattr(db_menu, key, value)

        db.commit()
        db.refresh(db_menu)

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="menu not found",
        )

    return db_menu


def delete_menu(db: Session, menu_id: UUID):
    db_menu = db.query(Menu).get(menu_id)

    if db_menu:
        db.delete(db_menu)
        db.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="menu not found",
        )

    return {"ok": True}
