from fastapi import FastAPI

from src.env import config

app = FastAPI()

MODE = config("MODE", default="dev-default")


@app.get("/")
def home_page():
    return {"Hello": "World", "mode": MODE}
