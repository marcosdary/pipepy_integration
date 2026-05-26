from pydantic import BeforeValidator, Field, AliasChoices
from typing import Annotated

# Schemas
from app.schemas.pipefy.field.base import (
    PipefyFieldBaseSchema
)
from app.schemas.validators import (
    validate_string_null
)

class PipefyFieldUpdateSchema(PipefyFieldBaseSchema):
    card_id: Annotated[
        str,
        BeforeValidator(validate_string_null),
        Field(
            validation_alias=AliasChoices("card_id", "cardId"),
            serialization_alias="cardId"
        )
    ]

    field_id: Annotated[
        str, 
        BeforeValidator(validate_string_null),
        Field(
            validation_alias=AliasChoices("fieldId", "field_id"),
            serialization_alias="fieldId"
        )
    ]
    new_value: Annotated[
        str, 
        BeforeValidator(validate_string_null),
        Field(
            validation_alias=AliasChoices("newValue", "new_value"),
            serialization_alias="newValue"
        )
    ]
     
    
