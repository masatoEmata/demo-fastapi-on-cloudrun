from fastapi.testclient import TestClient

from src.env import config
from src.main import app

MODE = config("MODE", default="dev")

client = TestClient(app)


def test_home_page():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World", "mode": MODE}
