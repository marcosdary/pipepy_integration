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
    """
    Schema utilizado para atualização de campos de um card no Pipefy.

    Este schema suporta múltiplos formatos de entrada (snake_case e camelCase)
    e garante padronização na serialização da saída.
    """

    card_id: Annotated[
        str,
        BeforeValidator(validate_string_null),
        Field(
            description="ID do card no Pipefy que será atualizado.",
            examples=["card_123"],
            validation_alias=AliasChoices("card_id", "cardId"),
            serialization_alias="cardId",
        )
    ]

    field_id: Annotated[
        str,
        BeforeValidator(validate_string_null),
        Field(
            description="ID do campo do Pipefy que será atualizado.",
            examples=["status"],
            validation_alias=AliasChoices("fieldId", "field_id"),
            serialization_alias="fieldId",
        )
    ]

    new_value: Annotated[
        str,
        BeforeValidator(validate_string_null),
        Field(
            description="Novo valor a ser atribuído ao campo.",
            examples=["Aprovado"],
            validation_alias=AliasChoices("newValue", "new_value"),
            serialization_alias="newValue",
        )
    ]