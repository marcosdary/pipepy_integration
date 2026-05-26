from http import HTTPStatus
from pytest import mark
from sqlalchemy import select

from app.models import CustomerModel
from app.schemas.customer import CustomerReadSchema

@mark.asyncio
async def test_error_event_processed(client):
    response = await client.post(
        "/api/v1/webhooks/pipefy/card-updated",
        json={
            "event_id": "evt_130",
            "card_id": "card_456",
            "cliente_email": "caio@exemplo.com",
            "timestamp": "2026-05-18T12:00:00Z"
        }
    )
    data: dict = response.json()
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
    data: dict = response.json()
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert data == {
            "detail": [
                {
                    "msg": "Value error, Campo não pode ser vazio"
                }
            ]
        }
    
@mark.asyncio
async def test_email_not_exist(client):
    
    response = await client.post(
        "/api/v1/webhooks/pipefy/card-updated",
        json={
            "event_id": "evt_103",
            "card_id": "card_456",
            "cliente_email": "caio.dutra@exemplo.com",
            "timestamp": "2026-05-18T12:00:00Z"
        }
    )
    data: dict = response.json()
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert data == {
        "detail": [
            {
                "msg": "Cliente não encontrado"
            }
        ]
    }

@mark.asyncio
async def test_applying_the_rule_of_equity(client, session, customer):
    before = CustomerReadSchema.model_validate(customer)
    
    response = await client.post(
        "/api/v1/webhooks/pipefy/card-updated",
        json={
            "event_id": "evt_104",
            "card_id": "card_456",
            "cliente_email": "caio.dutra@exemplo.com",
            "timestamp": "2026-05-18T12:00:00Z"
        }
    )

    customer = await session.scalar(
        select(CustomerModel)
        .where(CustomerModel.cliente_email == "caio.dutra@exemplo.com")
    )
    after = CustomerReadSchema.model_validate(customer)
    
    assert response.status_code == HTTPStatus.CREATED
    assert before.prioridade != after.prioridade
    assert after.status == "Processado"


