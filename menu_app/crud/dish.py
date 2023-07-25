from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from ..models.dish import Dish
from ..schemas import dish as dish_schema


def read_dishes(db: Session, submenu_id: UUID):
    return db.query(Dish).filter_by(submenu_id=submenu_id).all()


def read_dish(db: Session, submenu_id: UUID, dish_id: UUID):
    db_dish = (
        db.query(Dish).filter_by(submenu_id=submenu_id, id=dish_id).first()
    )

    if db_dish is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="dish not found",
        )

    return dish_schema.Dish(**db_dish.__dict__)


def create_dish(db: Session, submenu_id: UUID, dish: dish_schema.DishCreate):
    db_dish = Dish(
        submenu_id=submenu_id,
        title=dish.title,
        description=dish.description,
        price=dish.price,
    )

    db.add(db_dish)
    db.commit()

    db.refresh(db_dish)

    return dish_schema.Dish(**db_dish.__dict__)


def update_dish(
    db: Session,
    submenu_id: UUID,
    dish_id: UUID,
    dish: dish_schema.DishUpdate,
):
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
            detail="dish not found",
        )

    return dish_schema.Dish(**db_dish.__dict__)


def delete_dish(db: Session, submenu_id: UUID, dish_id: UUID):
    db_dish = (
        db.query(Dish).filter_by(submenu_id=submenu_id, id=dish_id).first()
    )

    if db_dish:
        db.delete(db_dish)

        db.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="dish not found",
        )

    return {"ok": True}
