
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException, Response, status

from ..models import models


def create(db: Session, recipe):
    db_recipe = models.Recipe(
        sandwich_id=recipe.sandwich_id,
        resource_id=recipe.resource_id,
        amount=recipe.amount
    )

    try:
        db.add(db_recipe)
        db.commit()
        db.refresh(db_recipe)
        return db_recipe
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Invalid sandwich or resource reference"
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error"
        )


def read_all(db: Session):
    return db.query(models.Recipe).all()


def read_one(db: Session, recipe_id: int):
    return (
        db.query(models.Recipe)
        .filter(models.Recipe.id == recipe_id)
        .first()
    )


def update(db: Session, recipe_id: int, recipe):
    db_recipe = read_one(db, recipe_id)

    if db_recipe is None:
        raise HTTPException(
            status_code=404,
            detail="Recipe not found"
        )

    update_data = recipe.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_recipe, key, value)

    try:
        db.commit()
        db.refresh(db_recipe)
        return db_recipe
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Invalid recipe reference or database constraint"
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error"
        )


def delete(db: Session, recipe_id: int):
    db_recipe = read_one(db, recipe_id)

    if db_recipe is None:
        raise HTTPException(
            status_code=404,
            detail="Recipe not found"
        )

    try:
        db.delete(db_recipe)
        db.commit()
        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Recipe cannot be deleted due to a database constraint"
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error"
        )
