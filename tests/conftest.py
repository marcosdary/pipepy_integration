from pytest_asyncio import fixture
from sqlalchemy.exc import IntegrityError
from pytest import raises
from httpx import AsyncClient, ASGITransport

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
async def client(session):
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
async def customer(session) -> CustomerModel:
    user = CustomerModel(
        cliente_nome = "Caio Fernando Dutra",
        cliente_email = "caio.dutra@exemplo.com",
        tipo_solicitacao = "Atualização cadastral",
        valor_patrimonio = 300000
    )
    session.add(user)
    with raises(IntegrityError):
        await session.commit()
        await session.refresh(user)
    await session.roolback()
        
    return user
