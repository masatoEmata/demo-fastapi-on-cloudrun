from fastapi import FastAPI

# from src.env import config
from gcloud_secret_configure.config import get_config
from gcloud_secret_configure.secret import GoogleSecretFetcher

app = FastAPI()

config = get_config(GoogleSecretFetcher())
MODE = config("MODE", cast=str, default="test")


@app.get("/")
def home_page():
    return {"Hello": "World", "mode": MODE}
