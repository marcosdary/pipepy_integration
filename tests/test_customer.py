from http import HTTPStatus
from pytest import mark

@mark.asyncio
async def test_index(client):
    response = await client.get("/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == { "version": "1.0.0", "name": "Integração com Pepify"}

@mark.asyncio
async def test_error_create_customer(client):
    response = await client.post(
        "/api/v1/clientes",
        json={
            "cliente_nome": "Lucas Santos",
            "cliente_email": "lucas@exemplo.com",
            "tipo_solicitacao": "Atualização cadastral",
            "valor_patrimonio": 300000
        }
    )
    data: dict = response.json()
    assert response.status_code == HTTPStatus.CONFLICT
    assert data == {
            "detail": [
                {
                    "msg": "Email está em uso."
                }
            ]
        }

@mark.asyncio
async def test_create_customer(client):
    response = await client.post(
        "/api/v1/clientes",
        json={
            "cliente_nome": "Caio Jorge",
            "cliente_email": "caio_jorge@exemplo.com",
            "tipo_solicitacao": "Atualização cadastral",
            "valor_patrimonio": 300000
        }
    )
    data: dict = response.json()
    assert response.status_code == HTTPStatus.CREATED
    assert data.get("cliente_nome") == "Caio Jorge"
    assert data.get("cliente_email") == "caio_jorge@exemplo.com"
    assert data.get("tipo_solicitacao") == "Atualização cadastral"
    assert data.get("valor_patrimonio") == 300000 

@mark.asyncio
async def test_error_email_create_customer(client):
    response = await client.post(
        "/api/v1/clientes",
        json={
            "cliente_nome": "Caio Jorge",
            "cliente_email": "caio_jorge@exemplo.com",
            "tipo_solicitacao": "Atualização cadastral",
            "valor_patrimonio": 300000
        }
    )
    data: dict = response.json()

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
            "valor_patrimonio": 300000
        }
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

