from functools import lru_cache
from typing import Optional
from zoneinfo import ZoneInfo

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)


class Settings(BaseSettings):
    """
    Configurações globais da aplicação.

    As variáveis são carregadas automaticamente
    a partir do arquivo `.env`.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # URL de conexão com o banco de dados
    DATABASE_URL: str

    # Fuso horário padrão da aplicação
    zone_info: Optional[ZoneInfo] = ZoneInfo(
        "America/Sao_Paulo"
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Retorna uma instância única das configurações.

    O uso de cache evita recriar o objeto
    Settings múltiplas vezes durante a execução.

    Returns:
        Settings:
            Instância das configurações da aplicação.
    """
    return Settings()


# Instância global das configurações
settings = get_settings()