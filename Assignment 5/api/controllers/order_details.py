
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException, Response, status

from ..models import models


def create(db: Session, order_detail):
    db_detail = models.OrderDetail(
        order_id=order_detail.order_id,
        sandwich_id=order_detail.sandwich_id,
        amount=order_detail.amount
    )

    try:
        db.add(db_detail)
        db.commit()
        db.refresh(db_detail)
        return db_detail
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Invalid order or sandwich reference"
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error"
        )


def read_all(db: Session):
    return db.query(models.OrderDetail).all()


def read_one(db: Session, order_detail_id: int):
    return (
        db.query(models.OrderDetail)
        .filter(models.OrderDetail.id == order_detail_id)
        .first()
    )


def update(db: Session, order_detail_id: int, order_detail):
    db_detail = read_one(db, order_detail_id)

    if db_detail is None:
        raise HTTPException(
            status_code=404,
            detail="Order detail not found"
        )

    update_data = order_detail.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_detail, key, value)

    try:
        db.commit()
        db.refresh(db_detail)
        return db_detail
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Invalid order or sandwich reference"
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error"
        )


def delete(db: Session, order_detail_id: int):
    db_detail = read_one(db, order_detail_id)

    if db_detail is None:
        raise HTTPException(
            status_code=404,
            detail="Order detail not found"
        )

    try:
        db.delete(db_detail)
        db.commit()
        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Order detail cannot be deleted due to a database constraint"
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error"
        )
