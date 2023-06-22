from fastapi import FastAPI

from src.env import config

app = FastAPI()

MODE = config("MODE", cast=str, default="test")


@app.get("/")
def home_page():
    return {"Hello": "World", "mode": MODE}
