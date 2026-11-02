from fastapi import FastAPI, HTTPException, status

from models.models import Sheep
from models.db import db


app = FastAPI()


@app.get("/sheep/{sheep_id}", response_model=Sheep)
def read_sheep(sheep_id: int):
    sheep = db.get_sheep(sheep_id)

    if sheep is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sheep not found"
        )

    return sheep


@app.post(
    "/sheep",
    response_model=Sheep,
    status_code=status.HTTP_201_CREATED
)
def add_sheep(sheep: Sheep):
    return db.add_sheep(sheep)