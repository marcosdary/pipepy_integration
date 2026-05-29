from pydantic import BeforeValidator, Field, AfterValidator, EmailStr
from typing import Annotated, Literal

from app.schemas.customer.base import (
    CustomerBaseSchema
)

from app.schemas.validators import (
    validate_asset_value,
    validate_string_null
)

class CustomerCreateSchema(CustomerBaseSchema):
    """
    Schema utilizado para criação de um cliente no sistema.

    Contém validações de dados e normalizações aplicadas antes da persistência.
    """

    cliente_nome: Annotated[
        str,
        BeforeValidator(validate_string_null)
    ] = Field(
        description="Nome do cliente.",
        examples=["João Silva"]
    )

    status: Annotated[
        Literal["Aguardando Análise"],
        Field(
            default="Aguardando Análise",
            frozen=True,
            description="Status inicial do cliente no fluxo de análise.",
            examples=["Aguardando Análise"]
        )
    ]

    cliente_email: Annotated[
        EmailStr,
        BeforeValidator(validate_string_null)
    ] = Field(
        description="E-mail do cliente em formato válido.",
        examples=["cliente@email.com"]
    )

    tipo_solicitacao: Annotated[
        str,
        BeforeValidator(validate_string_null)
    ] = Field(
        description="Tipo da solicitação realizada pelo cliente.",
        examples=["Abertura de conta"]
    )

    valor_patrimonio: Annotated[
        int,
        BeforeValidator(validate_asset_value)
    ] = Field(
        description="Valor do patrimônio informado pelo cliente (normalizado após validação).",
        examples=[1000000]
    )