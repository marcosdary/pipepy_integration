from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine
)
from sqlalchemy.orm import sessionmaker

from app.core.config.settings import settings

# Cria a engine assíncrona do SQLAlchemy
#
# Configurações utilizadas:
#   - pool_size:
#       Quantidade máxima de conexões persistentes abertas.
#
#   - max_overflow:
#       Quantidade extra de conexões permitidas em momentos de pico.
#
#   - pool_recycle:
#       Tempo em segundos para reciclar conexões antigas.
#
#   - pool_pre_ping:
#       Verifica se a conexão ainda está ativa antes de utilizá-la.
engine_async = create_async_engine(
    settings.DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
    pool_pre_ping=True,
)

# Factory responsável por criar sessões assíncronas
#
# expire_on_commit=False:
#   Mantém os objetos acessíveis após commit.
AsyncSessionLocal = sessionmaker(
    bind=engine_async,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator:
    """
    Fornece uma sessão assíncrona do banco de dados.

    Yields:
        AsyncSession:
            Sessão ativa do SQLAlchemy.
    """
    async with AsyncSessionLocal() as session:
        yield session