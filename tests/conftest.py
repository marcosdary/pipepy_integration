from datetime import datetime
from random import randint

from faker import Faker
from httpx import ASGITransport, AsyncClient
from pytest_asyncio import fixture
from sqlalchemy.ext.asyncio import AsyncSession

# Core
from app.core.config import settings
from app.core.config.database import (
    AsyncSessionLocal,
    engine_async,
    get_session
)

# Main
from app.main import app

# Models
from app.models import CustomerModel


@fixture(scope="function")
async def session():
    """
    Cria uma sessão assíncrona isolada para os testes.

    A fixture garante:
        - isolamento entre testes
        - rollback automático
        - fechamento correto das conexões

    Yields:
        AsyncSession:
            Sessão assíncrona do SQLAlchemy.
    """

    # Cria uma sessão exclusiva para o teste
    async with AsyncSessionLocal() as test_session:
        try:
            yield test_session

        finally:
            # Desfaz alterações realizadas durante o teste
            await test_session.rollback()

    # Fecha todas as conexões do pool
    await engine_async.dispose()


@fixture(scope="function")
def timestamp():
    """
    Gera um timestamp timezone-aware no formato ISO 8601.

    Returns:
        str:
            Data/hora atual formatada em ISO.
    """

    return datetime.now(
        settings.zone_info
    ).isoformat()


@fixture(scope="function")
async def client(session: AsyncSession):
    """
    Cria um cliente HTTP assíncrono para testes da API.

    A fixture:
        - sobrescreve a dependência get_session
        - utiliza a sessão de teste
        - executa requests sem subir servidor real

    Args:
        session:
            Sessão assíncrona do banco utilizada nos testes.

    Yields:
        AsyncClient:
            Cliente HTTP assíncrono configurado.
    """

    async def override_get_session():
        """
        Sobrescreve a dependência original da aplicação.

        Yields:
            AsyncSession:
                Sessão de teste.
        """
        yield session

    # Substitui a dependência original pelo banco de testes
    app.dependency_overrides[get_session] = override_get_session

    # Cliente HTTP ASGI em memória
    #
    # Não utiliza rede real nem sobe servidor HTTP.
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client

    # Limpa overrides para evitar vazamento entre testes
    app.dependency_overrides.clear()

    # Fecha conexões abertas do engine
    await engine_async.dispose()


@fixture(scope="function")
def customer_fake() -> Faker:
    """
    Cria uma instância do Faker configurada para pt_BR.

    Returns:
        Faker:
            Gerador de dados fake.
    """

    fake: Faker = Faker("pt_BR")

    return fake


@fixture(scope="function")
async def customer_model(
    session: AsyncSession,
    customer_fake: Faker
) -> CustomerModel:
    """
    Cria um cliente persistido no banco de testes.

    Args:
        session:
            Sessão assíncrona do banco.

        customer_fake:
            Instância do Faker utilizada para gerar dados.

    Returns:
        CustomerModel:
            Cliente salvo no banco.
    """

    # Cria entidade do cliente
    user = CustomerModel(
        cliente_nome=customer_fake.name(),
        cliente_email=customer_fake.email(),
        tipo_solicitacao="Atualização cadastral",
        valor_patrimonio=randint(100_000, 999_999)
    )

    # Adiciona cliente na sessão
    session.add(user)

    # Persiste dados no banco
    await session.commit()

    # Atualiza a instância ORM
    #
    # Necessário para carregar:
    #   - IDs gerados
    #   - defaults
    #   - valores atualizados
    await session.refresh(user)

    return user


@fixture(scope="function")
async def high_priority_customer(
    session: AsyncSession,
    customer_model: CustomerModel
) -> CustomerModel:
    """
    Cria um cliente com patrimônio suficiente
    para prioridade alta.

    Args:
        session:
            Sessão assíncrona do banco.

        customer_model:
            Cliente base previamente criado.

    Returns:
        CustomerModel:
            Cliente com alta prioridade.
    """

    # Define patrimônio alto
    customer_model.valor_patrimonio = randint(
        200_000,
        999_999
    )

    # Persiste alteração
    await session.commit()

    # Atualiza objeto ORM
    await session.refresh(customer_model)

    return customer_model


@fixture(scope="function")
async def low_priority_customer(
    session: AsyncSession,
    customer_model: CustomerModel
) -> CustomerModel:
    """
    Cria um cliente com patrimônio
    abaixo do limite de prioridade alta.

    Args:
        session:
            Sessão assíncrona do banco.

        customer_model:
            Cliente base previamente criado.

    Returns:
        CustomerModel:
            Cliente com prioridade normal.
    """

    # Define patrimônio baixo
    customer_model.valor_patrimonio = randint(
        0,
        199_999
    )

    # Persiste alteração
    await session.commit()

    # Atualiza objeto ORM
    await session.refresh(customer_model)

    return customer_model