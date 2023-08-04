from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..models.submenu import Submenu
from ..schemas import submenu as submenu_schema


def read_submenus(db: Session, menu_id: UUID):
    return db.query(Submenu).filter_by(menu_id=menu_id).all()


def read_submenu(db: Session, menu_id: UUID, submenu_id: UUID):
    db_submenu = (
        db.query(Submenu).filter_by(menu_id=menu_id, id=submenu_id).first()
    )

    if db_submenu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='submenu not found',
        )

    return submenu_schema.Submenu(**db_submenu.__dict__)


def create_submenu(
    db: Session,
    menu_id: UUID,
    submenu: submenu_schema.SubmenuCreate,
):
    db_submenu = Submenu(
        menu_id=menu_id,
        title=submenu.title,
        description=submenu.description,
    )

    db.add(db_submenu)
    db.commit()
    db.refresh(db_submenu)

    return submenu_schema.Submenu(**db_submenu.__dict__)


def update_submenu(
    db: Session,
    menu_id: UUID,
    submenu_id: UUID,
    submenu: submenu_schema.SubmenuUpdate,
):
    db_submenu = (
        db.query(Submenu).filter_by(menu_id=menu_id, id=submenu_id).first()
    )

    if db_submenu:
        db_submenu.title = submenu.title
        db_submenu.description = submenu.description

        db.commit()
        db.refresh(db_submenu)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='submenu not found',
        )

    return submenu_schema.Submenu(**db_submenu.__dict__)


def delete_submenu(db: Session, menu_id: UUID, submenu_id: UUID):
    db_submenu = (
        db.query(Submenu).filter_by(menu_id=menu_id, id=submenu_id).first()
    )

    if db_submenu:
        db.delete(db_submenu)
        db.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='submenu not found',
        )

    return {'ok': True}
