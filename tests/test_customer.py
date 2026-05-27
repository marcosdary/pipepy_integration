from http import HTTPStatus
from random import randint

from faker import Faker
from pytest import mark

# Models
from app.models import CustomerModel

# Schemas
from app.schemas.customer import (
    CustomerCreateSchema,
    CustomerReadSchema
)


@mark.asyncio
async def test_index(client):
    """
    Testa o endpoint raiz da aplicação.

    O teste valida:
        - status HTTP 200
        - estrutura da resposta
        - versão da API

    Args:
        client:
            Cliente HTTP assíncrono de testes.
    """

    # Realiza requisição GET no endpoint raiz
    response = await client.get("/")

    # Valida status HTTP
    assert response.status_code == HTTPStatus.OK

    # Valida payload retornado
    assert response.json() == {
        "version": "1.0.0",
        "name": "Integração com Pepify"
    }


@mark.asyncio
async def test_create_customer(
    client,
    customer_fake: Faker
):
    """
    Testa criação de cliente via API.

    O teste valida:
        - status HTTP 201
        - persistência dos dados
        - integridade do payload retornado

    Args:
        client:
            Cliente HTTP assíncrono.

        customer_fake:
            Instância do Faker para geração de dados.
    """

    # Cria payload de entrada
    schema: CustomerCreateSchema = CustomerCreateSchema(
        cliente_nome=customer_fake.name(),
        cliente_email=customer_fake.email(),
        tipo_solicitacao="Atualização cadastral",
        valor_patrimonio=randint(100_000, 999_999)
    )

    # Realiza requisição POST
    response = await client.post(
        "/api/v1/clientes",
        json=schema.model_dump()
    )

    data = response.json()

    # Valida status HTTP
    assert response.status_code == HTTPStatus.CREATED

    # Valida dados retornados
    assert data.get("cliente_nome") == schema.cliente_nome
    assert data.get("cliente_email") == schema.cliente_email
    assert data.get("tipo_solicitacao") == schema.tipo_solicitacao
    assert data.get("valor_patrimonio") == schema.valor_patrimonio


@mark.asyncio
async def test_error_email_create_customer(
    client,
    customer_model: CustomerModel
):
    """
    Testa erro de integridade ao tentar cadastrar
    cliente com e-mail já existente.

    O teste valida:
        - status HTTP 409
        - mensagem de erro padronizada

    Args:
        client:
            Cliente HTTP assíncrono.

        customer_model:
            Cliente previamente salvo no banco.
    """

    # Converte ORM para schema
    schema = CustomerReadSchema.model_validate(
        customer_model
    )

    # Realiza tentativa de cadastro duplicado
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

    # Valida status HTTP
    assert response.status_code == HTTPStatus.CONFLICT

    # Valida payload de erro
    assert data == {
        "detail": [
            {
                "msg": "Email está em uso."
            }
        ]
    }


@mark.asyncio
async def test_error_payload_create_customer(client):
    """
    Testa erro de validação do payload.

    O teste valida:
        - status HTTP 422
        - mensagens de validação
        - localização dos erros

    Cenários testados:
        - nome vazio
        - e-mail vazio
        - patrimônio inválido

    Args:
        client:
            Cliente HTTP assíncrono.
    """

    # Realiza requisição com payload inválido
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

    # Valida status HTTP
    assert (
        response.status_code
        == HTTPStatus.UNPROCESSABLE_ENTITY
    )

    # Valida estrutura do erro
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