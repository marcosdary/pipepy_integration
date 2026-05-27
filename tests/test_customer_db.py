from random import randint

from faker import Faker
from pytest import mark
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Models
from app.models import CustomerModel

# Schemas
from app.schemas.customer import (
    CustomerCreateSchema,
    CustomerReadSchema
)


@mark.asyncio
async def test_create(
    session: AsyncSession,
    customer_fake: Faker
):
    """
    Testa a criação de um cliente no banco de dados.

    O teste valida:
        - persistência do registro
        - integridade dos dados salvos
        - conversão ORM -> Schema

    Args:
        session:
            Sessão assíncrona do banco utilizada no teste.

        customer_fake:
            Instância do Faker para geração de dados.
    """

    # Cria schema de entrada
    schema: CustomerCreateSchema = CustomerCreateSchema(
        cliente_nome=customer_fake.name(),
        cliente_email=customer_fake.email(),
        tipo_solicitacao="Atualização cadastral",
        valor_patrimonio=randint(100_000, 999_999)
    )

    # Converte schema para dicionário
    customer_data = schema.model_dump()

    # Cria entidade ORM
    customer = CustomerModel(
        **customer_data
    )

    # Adiciona entidade na sessão
    session.add(customer)

    # Persiste dados no banco
    await session.commit()

    # Valida ORM utilizando schema de leitura
    data = CustomerReadSchema.model_validate(
        customer
    )

    # Valida dados persistidos
    assert data.cliente_nome == schema.cliente_nome
    assert data.cliente_email == schema.cliente_email
    assert data.tipo_solicitacao == schema.tipo_solicitacao
    assert data.valor_patrimonio == schema.valor_patrimonio


@mark.asyncio
async def test_error_integrity_create(
    session: AsyncSession,
    customer_model: CustomerModel
):
    """
    Testa integridade de dados ao verificar
    existência de cliente previamente salvo.

    O teste valida:
        - busca por e-mail
        - existência do registro no banco

    Args:
        session:
            Sessão assíncrona do banco.

        customer_model:
            Cliente previamente persistido.
    """

    # Converte entidade ORM para schema
    data = CustomerReadSchema.model_validate(
        customer_model
    )

    # Cria schema com os mesmos dados
    schema = CustomerCreateSchema(
        cliente_nome=data.cliente_nome,
        cliente_email=data.cliente_email,
        tipo_solicitacao=data.tipo_solicitacao,
        valor_patrimonio=data.valor_patrimonio
    )

    # Busca cliente pelo e-mail
    query = select(CustomerModel).where(
        CustomerModel.cliente_email == schema.cliente_email
    )

    stmt = await session.execute(query)

    customer = stmt.scalar_one_or_none()

    # Valida existência do cliente
    assert customer is not None
