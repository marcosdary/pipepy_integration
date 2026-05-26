from pydantic import BeforeValidator, EmailStr
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
    event_id: Annotated[str, BeforeValidator(validate_string_null)]
    card_id: Annotated[str, BeforeValidator(validate_string_null)]
    cliente_email: Annotated[EmailStr, BeforeValidator(validate_string_null)]
    timestamp: Annotated[datetime, BeforeValidator(validate_datetime)]



