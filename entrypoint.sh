#!/bin/bash

APP_PORT=${PORT:-8000}  # default port 8000
pipenv run uvicorn src.main:app --host 0.0.0.0 --port ${APP_PORT} --reload
