# python version
FROM python:3.10.12-slim

#  copy code, pipfile
COPY . /app/
WORKDIR /app/

# init apt-get and default installs
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    && rm -rf /var/lib/apt/lists/*

#  create pipenv environment
RUN pip install pipenv

# install dependencies in pipenv
RUN pipenv install --system --deploy

# run uvicorn server on pipenv environment
# CMD pipenv run uvicorn src.main:app
RUN chmod +x ./entrypoint.sh
CMD ["./entrypoint.sh"]
