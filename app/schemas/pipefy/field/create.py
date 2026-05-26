from pydantic import BeforeValidator, Field, AliasChoices
from typing import Annotated

# Schema
from app.schemas.pipefy.field.base import (
    PipefyFieldBaseSchema
)
from app.schemas.validators import (
    validate_string_null
)


class PipefyFieldCreateSchema(PipefyFieldBaseSchema):
    field_id: Annotated[
        str, 
        BeforeValidator(validate_string_null),
        Field(
            validation_alias=AliasChoices("fieldId", "field_id"),
            serialization_alias="fieldId"
        )
    ]
    field_value: Annotated[
        str, 
        BeforeValidator(validate_string_null),
        Field(
            validation_alias=AliasChoices("fieldValue", "field_value"),
            serialization_alias="fieldValue"
        )
    ]
     
    
