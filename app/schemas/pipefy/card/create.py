from pydantic import BeforeValidator, Field, AliasChoices
from typing import Annotated, List
from uuid import uuid4

# Schemas
from app.schemas.pipefy.card.base import (
    PipefyCardBaseSchema
)
from app.schemas.pipefy.field import PipefyFieldCreateSchema
from app.schemas.validators import (
    validate_string_null,
    validate_list
)

class PipefyCardCreateSchema(PipefyCardBaseSchema):
    pipe_id: Annotated[
        str, 
        BeforeValidator(validate_string_null), 
        Field(
            default_factory=lambda: str(uuid4()),
            validation_alias=AliasChoices("pipeId", "pipe_id"),
            serialization_alias="pipeId"
        )
    ]
    title: Annotated[
        str, 
        BeforeValidator(validate_string_null),
    ]
    fields_attributes: Annotated[
        List[PipefyFieldCreateSchema],
        BeforeValidator(validate_list),
        Field(
            validation_alias=AliasChoices("fieldsAttributes", "fields_attributes"),
            serialization_alias="fieldsAttributes",
        )
    ]
