
from .models import Sheep


class FakeDB:
    def __init__(self):
        self.data = {
            1: Sheep(
                id=1,
                name="Spice",
                breed="Gotland",
                sex="ewe"
            )
        }

    def get_sheep(self, sheep_id: int):
        return self.data.get(sheep_id)

    def add_sheep(self, sheep: Sheep):
        self.data[sheep.id] = sheep
        return sheep


db = FakeDB()