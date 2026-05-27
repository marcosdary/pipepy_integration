# Core
from app.core.constants import (
    PIPEFY_CARD_MUTATION,
    UPDATE_CARD_FIELDS
)

# Integrations
from app.integrations.pipefy.graphql import schema

# Schemas
from app.schemas.pipefy.card import PipefyCardCreateSchema
from app.schemas.pipefy.field import PipefyFieldUpdateSchema


class PipefyService:
    """
    Serviço responsável pela integração
    com a API GraphQL do Pipefy.
    """

    async def create_card(
        self,
        card: PipefyCardCreateSchema
    ):
        """
        Cria um novo card no Pipefy.

        Args:
            card:
                Dados necessários para criação
                do card.

        Returns:
            dict:
                Dados retornados pela API GraphQL.
        """

        # Define a mutation GraphQL
        mutation = PIPEFY_CARD_MUTATION

        # Define as variáveis enviadas para a mutation
        variables = {
            "input": card.model_dump(
                by_alias=True
            )
        }

        # Executa a mutation no Pipefy
        response = await schema.execute(
            mutation,
            variable_values=variables
        )

        return response.data

    async def update_card_field(
        self,
        status: PipefyFieldUpdateSchema,
        prioridade: PipefyFieldUpdateSchema
    ):
        """
        Atualiza os campos de status e prioridade
        de um card no Pipefy.

        Args:
            status:
                Dados de atualização do campo status.

            prioridade:
                Dados de atualização do campo prioridade.

        Returns:
            dict:
                Dados retornados pela API GraphQL.
        """

        # Define a mutation GraphQL
        mutation = UPDATE_CARD_FIELDS

        # Define as variáveis enviadas para a mutation
        variables = {
            "status": status.model_dump(
                by_alias=True
            ),
            "prioridade": prioridade.model_dump(
                by_alias=True
            )
        }

        # Executa a mutation no Pipefy
        response = await schema.execute(
            mutation,
            variable_values=variables
        )

        return response.data