from pydantic import BeforeValidator, EmailStr, Field
from typing import Annotated
from datetime import datetime

# Schemas
from app.schemas.pipefy.card.base import (
    PipefyCardBaseSchema,
    
)
from app.schemas.validators import (
    validate_string_null,
    validate_datetime
)


class PipefyCardUpdatedWebhookSchema(PipefyCardBaseSchema):
    """
    Schema utilizado para recebimento do webhook de atualização de card do Pipefy.

    Este payload é enviado pelo Pipefy sempre que um card é atualizado,
    contendo informações essenciais para rastreabilidade e processamento
    do evento no sistema.
    """

    event_id: Annotated[
        str,
        BeforeValidator(validate_string_null)
    ] = Field(
        description="Identificador único do evento enviado pelo Pipefy.",
        examples=["evt_130"]
    )

    card_id: Annotated[
        str,
        BeforeValidator(validate_string_null)
    ] = Field(
        description="Identificador do card atualizado no Pipefy.",
        examples=["card_456"]
    )

    cliente_email: Annotated[
        EmailStr,
        BeforeValidator(validate_string_null)
    ] = Field(
        description="E-mail do cliente associado ao card atualizado.",
        examples=["cliente@email.com"]
    )

    timestamp: Annotated[
        datetime,
        BeforeValidator(validate_datetime)
    ] = Field(
        description="Data e hora em que o evento foi gerado pelo Pipefy.",
        examples=["2026-05-27T12:00:00Z"]
    )
