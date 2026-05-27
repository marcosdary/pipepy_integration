from pytest_asyncio import fixture
from faker import Faker
from random import randint
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient, ASGITransport
from datetime import datetime

from app.core.config import settings
from app.models import CustomerModel
from app.core.config.database import AsyncSessionLocal, engine_async, get_session
from app.main import app


@fixture
async def session():
    async with AsyncSessionLocal() as test_session:
        try:
            yield test_session
        finally:
            await test_session.rollback()
    await engine_async.dispose()

@fixture
def timestamp():
    return datetime.now(settings.zone_info).isoformat()

@fixture
async def client(session: AsyncSession):
    async def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client

    app.dependency_overrides.clear()
    await engine_async.dispose()

@fixture
def customer_fake() -> Faker:
    fake: Faker = Faker('pt_BR')
    return fake

@fixture
async def customer_model(session: AsyncSession, customer_fake: Faker) -> CustomerModel:
    user = CustomerModel(
        cliente_nome = customer_fake.name(),
        cliente_email = customer_fake.email(),
        tipo_solicitacao = "Atualização cadastral",
        valor_patrimonio = randint(100_000, 999_999)
    )
    session.add(user)
    
    await session.commit()
    await session.refresh(user)
        
    return user

@fixture
async def high_priority_customer(session: AsyncSession, customer_model: CustomerModel) -> CustomerModel:
    customer_model.valor_patrimonio = randint(200_000, 999_999)
    await session.commit()
    await session.refresh(customer_model)
    return customer_model

@fixture
async def low_priority_customer(session: AsyncSession, customer_model: CustomerModel) -> CustomerModel:
    customer_model.valor_patrimonio = randint(0, 199_999)
    await session.commit()
    await session.refresh(customer_model)
    return customer_model


