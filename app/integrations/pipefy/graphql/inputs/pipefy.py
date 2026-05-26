from strawberry.experimental.pydantic import input as pydantic_input

from app.schemas.pipefy.card import PipefyCardCreateSchema
from app.schemas.pipefy.field import PipefyFieldCreateSchema, PipefyFieldUpdateSchema

@pydantic_input(PipefyFieldCreateSchema, all_fields=True)
class PipefyFieldInput: ...


@pydantic_input(PipefyCardCreateSchema, all_fields=True)
class PipefyCardInput: ...

@pydantic_input(PipefyFieldUpdateSchema, all_fields=True)
class PipefyFieldUpdateInput: ...

