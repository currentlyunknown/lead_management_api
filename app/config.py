from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str = None
    secret_key: str = None
    algorithm: str = None


settings = Settings()
