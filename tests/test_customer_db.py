from pytest import mark, raises
from sqlalchemy.exc import IntegrityError

from app.models import CustomerModel
from app.schemas.customer import CustomerCreateSchema, CustomerReadSchema


@mark.asyncio
async def test_create(session):
    schema = CustomerCreateSchema(
        cliente_nome = "Caio Fernando Dutra",
        cliente_email = "caio.dutra@exemplo.com",
        tipo_solicitacao = "Atualização cadastral",
        valor_patrimonio = 300000
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
async def test_error_integrity_create(session):
    schema = CustomerCreateSchema(
        cliente_nome = "Caio Fernando Dutra",
        cliente_email = "caio.dutra@exemplo.com",
        tipo_solicitacao = "Atualização cadastral",
        valor_patrimonio = 300000
    )
    customer_data = schema.model_dump()
    

    first_customer = CustomerModel(**customer_data)
    session.add(first_customer)
    await session.commit()
    
    duplicated_customer = CustomerModel(**customer_data)
    session.add(duplicated_customer)
    with raises(IntegrityError):
        await session.commit()
    await session.roolback()

