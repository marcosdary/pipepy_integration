from pydantic import EmailStr, Field
from datetime import datetime

from app.schemas.customer.base import (
    CustomerBaseSchema
)
from app.core.constants import Priority

class CustomerReadSchema(CustomerBaseSchema):
    """
    Schema de resposta utilizado para leitura de clientes.

    Representa os dados retornados pela API após criação ou consulta
    de um cliente, incluindo metadados de auditoria e status do fluxo.
    """

    cliente_nome: str = Field(
        description="Nome completo do cliente.",
        examples=["João Silva"]
    )

    cliente_email: EmailStr = Field(
        description="E-mail do cliente.",
        examples=["cliente@email.com"]
    )

    tipo_solicitacao: str = Field(
        description="Tipo de solicitação realizada pelo cliente.",
        examples=["Abertura de conta"]
    )

    valor_patrimonio: int = Field(
        description="Valor do patrimônio informado pelo cliente.",
        examples=[1000000]
    )

    status: str = Field(
        description="Status atual do cliente no fluxo de processamento.",
        examples=["Aguardando Análise"]
    )

    prioridade: Priority = Field(
        description="Prioridade atribuída ao cliente no sistema.",
        examples=["prioridade_alta"]
    )

    created_at: datetime = Field(
        description="Data de criação do registro.",
        examples=["2026-05-27T12:00:00Z"]
    )

    updated_at: datetime = Field(
        description="Data da última atualização do registro.",
        examples=["2026-05-27T12:30:00Z"]
    )


