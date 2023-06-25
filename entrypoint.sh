#!/bin/bash

APP_PORT=${PORT:-8080}  # default port 8080
pipenv run uvicorn src.main:app --host 0.0.0.0 --port ${APP_PORT} --reload
