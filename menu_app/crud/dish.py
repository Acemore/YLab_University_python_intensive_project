from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..models.dish import Dish
from ..schemas.dish import Dish as DishSchema
from ..schemas.dish import DishCreate, DishUpdate


def read_dishes(db: Session, submenu_id: UUID) -> list[DishSchema]:
    return db.query(Dish).filter_by(submenu_id=submenu_id).all()


def read_dish(db: Session, submenu_id: UUID, dish_id: UUID) -> DishSchema:
    db_dish = (
        db.query(Dish).filter_by(submenu_id=submenu_id, id=dish_id).first()
    )

    if db_dish is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='dish not found',
        )

    return DishSchema(**db_dish.__dict__)


def create_dish(db: Session, submenu_id: UUID, dish: DishCreate) -> DishSchema:
    db_dish = Dish(
        submenu_id=submenu_id,
        title=dish.title,
        description=dish.description,
        price=dish.price,
    )

    db.add(db_dish)
    db.commit()

    db.refresh(db_dish)

    return DishSchema(**db_dish.__dict__)


def update_dish(
    db: Session,
    submenu_id: UUID,
    dish_id: UUID,
    dish: DishUpdate,
) -> DishSchema:
    db_dish = (
        db.query(Dish).filter_by(submenu_id=submenu_id, id=dish_id).first()
    )

    if db_dish:
        db_dish.title = dish.title
        db_dish.description = dish.description
        db_dish.price = dish.price

        db.commit()
        db.refresh(db_dish)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='dish not found',
        )

    return DishSchema(**db_dish.__dict__)


def delete_dish(db: Session, submenu_id: UUID, dish_id: UUID) -> dict[str, bool]:
    db_dish = (
        db.query(Dish).filter_by(submenu_id=submenu_id, id=dish_id).first()
    )

    if db_dish:
        db.delete(db_dish)

        db.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='dish not found',
        )

    return {'ok': True}
