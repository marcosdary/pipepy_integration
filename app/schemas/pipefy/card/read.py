from pydantic import BeforeValidator, Field, AliasChoices
from typing import Annotated
from uuid import uuid4

# Schemas
from app.schemas.pipefy.card.base import (
    PipefyCardBaseSchema,
)
from app.schemas.validators import (
    validate_string_null,
)

class PipefyCardReadSchema(PipefyCardBaseSchema):
    pipe_id: Annotated[
        str, 
        BeforeValidator(validate_string_null),
        Field(
            default_factory=lambda: str(uuid4()),
            validation_alias=AliasChoices("pipeId", "pipe_id"),
            serialization_alias="pipeId"
        )  
    ] 
    title: Annotated[str, BeforeValidator(validate_string_null)]
