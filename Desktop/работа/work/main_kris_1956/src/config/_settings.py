from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn

from src.constants import BASE_DIR


class Settings(BaseSettings):
    name: str
    api_id: int
    api_hash: str
    phone: str

    postgres_dsn: PostgresDsn

    model_config = SettingsConfigDict(env_file=BASE_DIR / '.env', env_file_encoding="utf-8", extra="ignore")


settings = Settings()
