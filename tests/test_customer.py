from http import HTTPStatus
from pytest import mark
from faker import Faker
from random import randint
from random import randint

from app.schemas.customer import (
    CustomerCreateSchema,
    CustomerReadSchema
)
from app.models import CustomerModel

@mark.asyncio
async def test_index(client):
    response = await client.get("/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == { "version": "1.0.0", "name": "Integração com Pepify"}

@mark.asyncio
async def test_create_customer(client, customer_fake: Faker):
    schema: CustomerCreateSchema = CustomerCreateSchema(
        cliente_nome=customer_fake.name(),
        cliente_email=customer_fake.email(),
        tipo_solicitacao="Atualização cadastral",
        valor_patrimonio=randint(100_000, 999_999)
    )

    response = await client.post(
        "/api/v1/clientes",
        json=schema.model_dump()
    )
    data = response.json()
    assert response.status_code == HTTPStatus.CREATED
    assert data.get("cliente_nome") == schema.cliente_nome
    assert data.get("cliente_email") == schema.cliente_email
    assert data.get("tipo_solicitacao") == schema.tipo_solicitacao
    assert data.get("valor_patrimonio") == schema.valor_patrimonio

@mark.asyncio
async def test_error_email_create_customer(client, customer_model: CustomerModel):
    schema = CustomerReadSchema.model_validate(customer_model)
    response = await client.post(
        "/api/v1/clientes",
        json={
            "cliente_nome": schema.cliente_nome,
            "cliente_email": schema.cliente_email,
            "tipo_solicitacao": "Atualização cadastral",
            "valor_patrimonio": randint(100_000, 999_999)
        }
    )
    data = response.json()

    assert response.status_code == HTTPStatus.CONFLICT
    assert data == {
            "detail": [
                {
                    "msg": "Email está em uso."
                }
            ]
        }

@mark.asyncio
async def test_error_payload_create_customer(client):
    response = await client.post(
        "/api/v1/clientes",
        json={
            "cliente_nome": "",
            "cliente_email": "",
            "tipo_solicitacao": "Atualização cadastral",
            "valor_patrimonio": -300000
        }
    )

    data = response.json()
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert data == {
            "detail": [
                {
                    "msg": "Value error, Campo não pode ser vazio",
                    "loc": [
                        "body",
                        "cliente_nome"
                    ]
                },
                {
                    "msg": "Value error, Campo não pode ser vazio",
                    "loc": [
                        "body",
                        "cliente_email"
                    ]
                },
                {
                    "msg": "Value error, O valor de patrimônio inválido.",
                    "loc": [
                        "body",
                        "valor_patrimonio"
                    ]
                }
            ]
        }
