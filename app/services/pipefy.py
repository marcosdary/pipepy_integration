from app.schemas.pipefy.card import PipefyCardCreateSchema
from app.schemas.pipefy.field import PipefyFieldUpdateSchema
from app.core.constants import (
    PIPEFY_CARD_MUTATION,
    UPDATE_CARD_FIELDS
)
from app.integrations.pipefy.graphql import schema

class PipefyService:
    async def create_card(self, card: PipefyCardCreateSchema):
        mutation = PIPEFY_CARD_MUTATION
        variables = {
            "input": card.model_dump(by_alias=True)
        }
        response = await schema.execute(mutation, variable_values=variables)
        return response.data
    
    async def update_card_field(
        self, 
        status: PipefyFieldUpdateSchema, 
        prioridade: PipefyFieldUpdateSchema
    ):
        mutation = UPDATE_CARD_FIELDS
        variables = {
            "status": status.model_dump(by_alias=True),
            "prioridade": prioridade.model_dump(by_alias=True)
        }
        response = await schema.execute(mutation, variable_values=variables)
        return response.data
    
