import strawberry

from app.schemas.pipefy.payload import PipefyPayloadSchema
from app.integrations.pipefy.graphql.inputs import (
    PipefyCardInput,
    PipefyFieldUpdateInput
)
from app.integrations.pipefy.graphql.types import (
    PipefyPayloadType
)

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_card(self, input: PipefyCardInput) -> PipefyPayloadType:
        data = input.to_pydantic()
        return PipefyPayloadSchema(card=data.model_dump())

    @strawberry.mutation
    def update_card_field(self, input: PipefyFieldUpdateInput) -> PipefyPayloadType:
        data = input.to_pydantic()
        return PipefyPayloadSchema(success=True)