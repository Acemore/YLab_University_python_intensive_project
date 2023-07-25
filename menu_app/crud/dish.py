from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from ..models.dish import Dish
from ..models.menu import Menu
from ..models.submenu import Submenu
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

    db_dish.submenu.dishes_count += 1
    db_dish.submenu.menu.dishes_count += 1

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
        dish_data = dish.dict()

        for key, value in dish_data.items():
            setattr(db_dish, key, value)

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

        db.query(Submenu).filter_by(id=submenu_id).first().dishes_count -= 1
        db.query(Menu).join(Submenu).filter(
            Submenu.id == submenu_id).first().dishes_count -= 1

        db.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="dish not found",
        )

    return {"ok": True}
