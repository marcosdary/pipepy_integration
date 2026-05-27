from http import HTTPStatus
from random import randint

from pytest import mark
from sqlalchemy import select

# Core
from app.core.constants import Priority

# Models
from app.models import CustomerModel

# Schemas
from app.schemas.customer import CustomerReadSchema


@mark.asyncio
async def test_error_event_processed(
    client,
    timestamp
):
    """
    Testa erro ao tentar processar
    um evento já processado.

    O teste valida:
        - status HTTP 403
        - mensagem de erro padronizada

    Args:
        client:
            Cliente HTTP assíncrono.

        timestamp:
            Timestamp válido em formato ISO.
    """

    # Realiza requisição utilizando
    # evento previamente processado
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

    # Valida status HTTP
    assert response.status_code == HTTPStatus.FORBIDDEN

    # Valida payload de erro
    assert data == {
        "detail": [
            {
                "msg": "Evento já processado"
            }
        ]
    }


@mark.asyncio
async def test_error_event_fields_null(client):
    """
    Testa erro de validação quando
    campos obrigatórios estão vazios.

    O teste valida:
        - status HTTP 422
        - mensagem de validação
        - localização do erro

    Args:
        client:
            Cliente HTTP assíncrono.
    """

    # Realiza requisição com campo inválido
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

    # Valida status HTTP
    assert (
        response.status_code
        == HTTPStatus.UNPROCESSABLE_ENTITY
    )

    # Valida payload de erro
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
    """
    Testa erro quando o cliente informado
    não existe no banco de dados.

    O teste valida:
        - status HTTP 404
        - mensagem de erro padronizada

    Args:
        client:
            Cliente HTTP assíncrono.
    """

    # Gera identificador único do evento
    event_id = f"evt_{randint(10_000, 99_999)}"

    # Realiza requisição utilizando
    # e-mail inexistente
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

    # Valida status HTTP
    assert response.status_code == HTTPStatus.NOT_FOUND

    # Valida payload de erro
    assert data == {
        "detail": [
            {
                "msg": "Cliente não encontrado"
            }
        ]
    }


@mark.asyncio
async def test_applying_high_priority_customer(
    client,
    session,
    high_priority_customer: CustomerModel
):
    """
    Testa aplicação automática de prioridade alta.

    O teste valida:
        - processamento do webhook
        - atualização da prioridade
        - atualização do status do cliente

    Cenário:
        Cliente possui patrimônio >= 200.000.

    Args:
        client:
            Cliente HTTP assíncrono.

        session:
            Sessão assíncrona do banco.

        high_priority_customer:
            Cliente configurado com patrimônio alto.
    """

    # Salva estado anterior do cliente
    before = CustomerReadSchema.model_validate(
        high_priority_customer
    )

    # Gera identificador único do evento
    event_id = f"evt_{randint(10_000, 99_999)}"

    # Realiza processamento do webhook
    response = await client.post(
        "/api/v1/webhooks/pipefy/card-updated",
        json={
            "event_id": event_id,
            "card_id": "card_456",
            "cliente_email": before.cliente_email,
            "timestamp": "2026-05-18T12:00:00Z"
        }
    )

    # Recarrega cliente atualizado no banco
    high_priority_customer = await session.scalar(
        select(CustomerModel).where(
            CustomerModel.cliente_email
            == before.cliente_email
        )
    )

    # Converte ORM para schema
    after = CustomerReadSchema.model_validate(
        high_priority_customer
    )

    # Valida sucesso da operação
    assert response.status_code == HTTPStatus.CREATED

    # Valida prioridade aplicada
    assert (
        after.prioridade
        == Priority.prioridade_alta
    )

    # Valida status atualizado
    assert after.status == "Processado"


@mark.asyncio
async def test_applying_low_priority_customer(
    client,
    session,
    low_priority_customer: CustomerModel
):
    """
    Testa aplicação automática de prioridade normal.

    O teste valida:
        - processamento do webhook
        - atualização da prioridade
        - atualização do status do cliente

    Cenário:
        Cliente possui patrimônio < 200.000.

    Args:
        client:
            Cliente HTTP assíncrono.

        session:
            Sessão assíncrona do banco.

        low_priority_customer:
            Cliente configurado com patrimônio baixo.
    """

    # Salva estado anterior do cliente
    before = CustomerReadSchema.model_validate(
        low_priority_customer
    )

    # Gera identificador único do evento
    event_id = f"evt_{randint(10_000, 99_999)}"

    # Realiza processamento do webhook
    response = await client.post(
        "/api/v1/webhooks/pipefy/card-updated",
        json={
            "event_id": event_id,
            "card_id": "card_456",
            "cliente_email": before.cliente_email,
            "timestamp": "2026-05-18T12:00:00Z"
        }
    )

    # Recarrega cliente atualizado no banco
    low_priority_customer = await session.scalar(
        select(CustomerModel).where(
            CustomerModel.cliente_email
            == before.cliente_email
        )
    )

    # Converte ORM para schema
    after = CustomerReadSchema.model_validate(
        low_priority_customer
    )

    # Valida sucesso da operação
    assert response.status_code == HTTPStatus.CREATED

    # Valida prioridade aplicada
    assert (
        after.prioridade
        == Priority.prioridade_normal
    )

    # Valida status atualizado
    assert after.status == "Processado"