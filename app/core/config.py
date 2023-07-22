from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):

    PG_DRIVER: str
    PG_USER: str
    PG_PASSWORD: str
    PG_HOST: str
    PG_PORT: int
    PG_DB: str
    PG_NOTIFICATION_SCHEMA: str
    PG_USER_SCHEMA: str
    PG_POKEMON_SCHEMA: str
    PG_DEBUG_FLAG: bool
    PG_AUTOFLUSH: bool
    PG_AUTOCOMMIT: bool

    API_PORT: int
    API_HOST: str
    API_WORKERS: int
    API_DEBUG_LEVEL: str
    API_CORS_ORIGINS: List

    SSL_CERTFILE:str
    SSL_KEYFILE:str

    JWT_SECRET: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()