from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_read_sheep():
    response = client.get("/sheep/1")

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Spice",
        "breed": "Gotland",
        "sex": "ewe"
    }


def test_add_sheep():
    sheep_data = {
        "id": 2,
        "name": "Dolly",
        "breed": "Suffolk",
        "sex": "ewe"
    }

    response = client.post("/sheep", json=sheep_data)

    assert response.status_code == 201
    assert response.json() == sheep_data