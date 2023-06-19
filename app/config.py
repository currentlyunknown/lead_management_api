import logging

from pydantic import BaseSettings

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    database_url: str = None
    secret_key: str = None
    algorithm: str = None


def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()
