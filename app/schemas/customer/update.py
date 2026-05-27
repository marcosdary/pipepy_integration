from pydantic import BeforeValidator, Field, AfterValidator, EmailStr
from typing import Annotated, Optional

# Schema
from app.schemas.customer.base import (
    CustomerBaseSchema,
)

from app.schemas.validators import (
    validate_string_null
)

# Core
from app.core.constants import Priority

class CustomerUpdateSchema(CustomerBaseSchema):
    cliente_email: Annotated[EmailStr, BeforeValidator(validate_string_null)]
    status: Annotated[Optional[str], Field(default="Processado")]
    prioridade: Annotated[Priority, Field(default=Priority.prioridade_normal)]




