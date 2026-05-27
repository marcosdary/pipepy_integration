from pytest import mark, raises
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from faker import Faker
from random import randint

from app.models import CustomerModel
from app.schemas.customer import CustomerCreateSchema, CustomerReadSchema


@mark.asyncio
async def test_create(session: AsyncSession, customer_fake: Faker):
    schema: CustomerCreateSchema = CustomerCreateSchema(
        cliente_nome=customer_fake.name(),
        cliente_email=customer_fake.email(),
        tipo_solicitacao="Atualização cadastral",
        valor_patrimonio=randint(100_000, 999_999)
    )
    customer_data = schema.model_dump()
    customer = CustomerModel(**customer_data)
    
    session.add(customer)
   
    await session.commit()

    data = CustomerReadSchema.model_validate(customer)

    assert data.cliente_nome == schema.cliente_nome
    assert data.cliente_email == schema.cliente_email
    assert data.tipo_solicitacao == schema.tipo_solicitacao
    assert data.valor_patrimonio == schema.valor_patrimonio


@mark.asyncio
async def test_error_integrity_create(session, customer_model: CustomerModel):
    data = CustomerReadSchema.model_validate(customer_model)
    schema = CustomerCreateSchema(
        cliente_nome = data.cliente_nome,
        cliente_email = data.cliente_email,
        tipo_solicitacao = data.tipo_solicitacao,
        valor_patrimonio = data.valor_patrimonio
    )

    query = select(CustomerModel).where(
        CustomerModel.cliente_email == schema.cliente_email
    )

    stmt = await session.execute(query)

    customer = stmt.scalar_one_or_none()

    assert customer is not None


