import io
import os
import pathlib
from functools import lru_cache

import google.auth
from decouple import Config, RepositoryEmpty, RepositoryEnv
from google.cloud import secretmanager

BASE_DIR = pathlib.Path(__file__).parent
ENV_PATH = BASE_DIR / ".env"


def get_google_secret_payload(secret_label="env_file", version="latest") -> str | None:
    try:
        _, project_id = google.auth.default()
    except google.auth.exceptions.DefaultCredentialsError:
        project_id = None
    if project_id is None:
        return None

    client = secretmanager.SecretManagerServiceClient()

    # my_secret_file is the name of the secret you
    # set with `gcloud secrets create {{GCLOUD_SECRET_LABEL}}....`
    # project_id comes from previous step
    secret_label = os.environ.get("GCLOUD_SECRET_LABEL", secret_label)
    version = os.environ.get("GCLOUD_SECRET_VERSION", version)
    gcloud_secret_name = (
        f"projects/{project_id}/secrets/{secret_label}/versions/{version}"
    )

    # this should print the contents of your secret
    payload = client.access_secret_version(name=gcloud_secret_name).payload.data.decode(
        "UTF-8"
    )
    return payload


class RepositoryString(RepositoryEmpty):
    """
    Retrieves option keys from an ENV string file
    """

    def __init__(self, source):
        """
        Take a string source with the dotenv file format:

        KEY=value

        Then parse it into a dictionary
        """
        source = io.StringIO(source)
        if not isinstance(source, io.StringIO):
            raise ValueError("source must be an instance of io.StringIO")
        self.data = {}
        file_ = source.read().split("\n")
        for line in file_:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k = k.strip()
            v = v.strip()
            if len(v) >= 2 and (
                (v[0] == "'" and v[-1] == "'") or (v[0] == '"' and v[-1] == '"')
            ):
                v = v[1:-1]
            self.data[k] = v

    def __contains__(self, key):
        return key in os.environ or key in self.data

    def __getitem__(self, key):
        return self.data[key]


@lru_cache()
def get_config(use_gcloud=True):
    if ENV_PATH.exists():
        return Config(RepositoryEnv(str(ENV_PATH)))

    if use_gcloud:
        payload = get_google_secret_payload()
        if payload is not None:
            return Config(RepositoryString(payload))

    from decouple import config

    return config


config = get_config()
# sample usage:
# from src.env import config
# MODE = config("MODE", cast=str, default="default")
