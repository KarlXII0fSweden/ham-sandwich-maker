
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException, Response, status

from ..models import models


def create(db: Session, sandwich):
    db_sandwich = models.Sandwich(
        sandwich_name=sandwich.sandwich_name,
        price=sandwich.price
    )

    try:
        db.add(db_sandwich)
        db.commit()
        db.refresh(db_sandwich)
        return db_sandwich
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Sandwich already exists or violates a database constraint"
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error"
        )


def read_all(db: Session):
    return db.query(models.Sandwich).all()


def read_one(db: Session, sandwich_id: int):
    return (
        db.query(models.Sandwich)
        .filter(models.Sandwich.id == sandwich_id)
        .first()
    )


def update(db: Session, sandwich_id: int, sandwich):
    db_sandwich = read_one(db, sandwich_id)

    if db_sandwich is None:
        raise HTTPException(
            status_code=404,
            detail="Sandwich not found"
        )

    update_data = sandwich.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_sandwich, key, value)

    try:
        db.commit()
        db.refresh(db_sandwich)
        return db_sandwich
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Update violates a database constraint"
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error"
        )


def delete(db: Session, sandwich_id: int):
    db_sandwich = read_one(db, sandwich_id)

    if db_sandwich is None:
        raise HTTPException(
            status_code=404,
            detail="Sandwich not found"
        )

    try:
        db.delete(db_sandwich)
        db.commit()
        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Sandwich is referenced by another record"
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error"
        )
