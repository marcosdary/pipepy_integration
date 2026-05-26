from pydantic import BeforeValidator, Field, AfterValidator, EmailStr
from typing import Annotated, Optional

from app.schemas.customer.base import (
    CustomerBaseSchema
)

from app.schemas.validators import (
    validate_asset_value,
    validate_string_null
)

class CustomerCreateSchema(CustomerBaseSchema):
    cliente_nome: Annotated[str, BeforeValidator(validate_string_null)]
    status: Optional[str] = Field(default="Aguardando Análise")
    cliente_email: Annotated[EmailStr, BeforeValidator(validate_string_null)]
    tipo_solicitacao: Annotated[str, BeforeValidator(validate_string_null)]
    valor_patrimonio: Annotated[
        int, 
        BeforeValidator(validate_string_null), 
        AfterValidator(validate_asset_value)
    ]








