from http import HTTPStatus
from pytest import mark
from sqlalchemy import select
from random import randint

from app.models import CustomerModel
from app.schemas.customer import CustomerReadSchema

@mark.asyncio
async def test_error_event_processed(client, timestamp):
    response = await client.post(
        "/api/v1/webhooks/pipefy/card-updated",
        json={
            "event_id": "evt_130",
            "card_id": "card_456",
            "cliente_email": "caio@exemplo.com",
            "timestamp": timestamp
        }
    )
    data = response.json()
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert data == {
            "detail": [
                {
                    "msg": "Evento já processado"
                }
            ]
        }

@mark.asyncio
async def test_error_event_fields_null(client):
    response = await client.post(
        "/api/v1/webhooks/pipefy/card-updated",
        json={
            "event_id": "",
            "card_id": "card_456",
            "cliente_email": "caio@exemplo.com",
            "timestamp": "2026-05-18T12:00:00Z"
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
                        "event_id"
                    ]
                }
            ]
        }
    
@mark.asyncio
async def test_email_not_exist(client):
    event_id = f"evt_{randint(10_000, 99_999)}"

    response = await client.post(
        "/api/v1/webhooks/pipefy/card-updated",
        json={
            "event_id": event_id,
            "card_id": "card_456",
            "cliente_email": "email.nao.existe@exemplo.com",
            "timestamp": "2026-05-18T12:00:00Z"
        }
    )
    data = response.json()
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert data == {
        "detail": [
            {
                "msg": "Cliente não encontrado"
            }
        ]
    }

@mark.asyncio
async def test_applying_the_rule_of_equity(client, session, customer_model: CustomerModel):
    before = CustomerReadSchema.model_validate(customer_model)
    event_id = f"evt_{randint(10_000, 99_999)}"
    response = await client.post(
        "/api/v1/webhooks/pipefy/card-updated",
        json={
            "event_id": event_id,
            "card_id": "card_456",
            "cliente_email": before.cliente_email,
            "timestamp": "2026-05-18T12:00:00Z"
        }
    )

    customer_model = await session.scalar(
        select(CustomerModel)
        .where(CustomerModel.cliente_email == before.cliente_email)
    )
    after = CustomerReadSchema.model_validate(customer_model)
    
    assert response.status_code == HTTPStatus.CREATED
    assert before.prioridade != after.prioridade
    assert after.status == "Processado"


