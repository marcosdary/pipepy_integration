from strawberry.experimental.pydantic import type as pydantic_type

from app.schemas.pipefy.card import PipefyCardReadSchema
from app.schemas.pipefy.payload import PipefyPayloadSchema

@pydantic_type(PipefyCardReadSchema, all_fields=True)
class PipefyCardType: ...

@pydantic_type(PipefyPayloadSchema, all_fields=True)
class PipefyPayloadType: ...

