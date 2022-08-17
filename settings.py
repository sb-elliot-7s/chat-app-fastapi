from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    secret_key: str

    db_url: str
    postgres_user: str
    postgres_password: str
    postgres_db_name: str
    postgres_server: str
    postgres_port: int

    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


@lru_cache
def get_settings() -> Settings:
    return Settings()
