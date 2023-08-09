from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..models.submenu import Submenu
from ..schemas.submenu import Submenu as SubmenuSchema
from ..schemas.submenu import SubmenuCreate, SubmenuUpdate


def read_submenus(db: Session, menu_id: UUID) -> list[SubmenuSchema]:
    return db.query(Submenu).filter_by(menu_id=menu_id).all()


def read_submenu(db: Session, menu_id: UUID, submenu_id: UUID) -> SubmenuSchema:
    db_submenu = (
        db.query(Submenu).filter_by(menu_id=menu_id, id=submenu_id).first()
    )

    if db_submenu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='submenu not found',
        )

    return SubmenuSchema(**db_submenu.__dict__)


def create_submenu(
    db: Session,
    menu_id: UUID,
    submenu: SubmenuCreate,
) -> SubmenuSchema:
    db_submenu = Submenu(
        menu_id=menu_id,
        title=submenu.title,
        description=submenu.description,
    )

    db.add(db_submenu)
    db.commit()
    db.refresh(db_submenu)

    return SubmenuSchema(**db_submenu.__dict__)


def update_submenu(
    db: Session,
    menu_id: UUID,
    submenu_id: UUID,
    submenu: SubmenuUpdate,
) -> SubmenuSchema:
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

    return SubmenuSchema(**db_submenu.__dict__)


def delete_submenu(db: Session, menu_id: UUID, submenu_id: UUID) -> dict[str, bool]:
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
