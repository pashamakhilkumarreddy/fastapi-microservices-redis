from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    redis_host: str
    redis_port: int
    redis_password: str

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
