from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    REDIS_URL: str

    ACCESS_KEY: str
    SECRET_KEY: str
    ENDPOINT_URL: str
    BUCKET_NAME: str

    SECRET_KEY_FOR_JWT: str
    ALGORITHM: str

    class Config:
        env_file = ".env"


settings = Settings()
