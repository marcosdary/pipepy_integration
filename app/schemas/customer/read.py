from pydantic import EmailStr
from datetime import datetime

from app.schemas.customer.base import (
    CustomerBaseSchema
)
from app.core.constants import Priority

class CustomerReadSchema(CustomerBaseSchema):
    cliente_nome: str
    cliente_email: EmailStr
    tipo_solicitacao: str
    valor_patrimonio: int
    status: str
    prioridade: Priority
    created_at: datetime
    updated_at: datetime



