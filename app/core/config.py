"""_summary_
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """_summary_

    Args:
        BaseSettings (_type_): _description_
    """

    PROJECT_NAME: str

    PG_HOST: str
    PG_DB: str
    PG_PORT: int
    PG_USERNAME: str
    PG_PASSWORD: str
    PG_DRIVER: str
    PG_DEBUG_FLAG: bool
    PG_AUTOFLUSH: bool

    API_HOST: str
    API_ALLOW_ORIGINS: str
    API_PORT: int
    API_WORKERS: int
    API_DEBUG_MODE: bool
    API_DEBUG_LEVEL: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int
    JWT_SECRET: str
    ALGORITHM: str

    SMTP_HOST: str
    EMAIL_FROM: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
