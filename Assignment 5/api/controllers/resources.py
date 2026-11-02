
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException, Response, status

from ..models import models


def create(db: Session, resource):
    db_resource = models.Resource(
        item=resource.item,
        amount=resource.amount
    )

    try:
        db.add(db_resource)
        db.commit()
        db.refresh(db_resource)
        return db_resource
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Resource already exists or violates a database constraint"
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error"
        )


def read_all(db: Session):
    return db.query(models.Resource).all()


def read_one(db: Session, resource_id: int):
    return (
        db.query(models.Resource)
        .filter(models.Resource.id == resource_id)
        .first()
    )


def update(db: Session, resource_id: int, resource):
    db_resource = read_one(db, resource_id)

    if db_resource is None:
        raise HTTPException(
            status_code=404,
            detail="Resource not found"
        )

    update_data = resource.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_resource, key, value)

    try:
        db.commit()
        db.refresh(db_resource)
        return db_resource
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


def delete(db: Session, resource_id: int):
    db_resource = read_one(db, resource_id)

    if db_resource is None:
        raise HTTPException(
            status_code=404,
            detail="Resource not found"
        )

    try:
        db.delete(db_resource)
        db.commit()
        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Resource is referenced by another record"
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error"
        )
