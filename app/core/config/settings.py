from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from zoneinfo import ZoneInfo
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    DATABASE_URL: str
    zone_info: Optional[ZoneInfo] = ZoneInfo("America/Sao_Paulo") 


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()

settings = get_settings()

