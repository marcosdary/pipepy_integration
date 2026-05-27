from uuid import uuid4

from sqlalchemy.orm import Mapped, mapped_column

from app.core.constants import Priority
from app.models.base import BaseModel


class CustomerModel(BaseModel):
    """
    Modelo responsável por representar os clientes no banco de dados.

    Attributes:
        customer_id:
            Identificador único do cliente.

        cliente_nome:
            Nome completo do cliente.

        prioridade:
            Prioridade atribuída ao cliente.

        status:
            Status atual do processo do cliente.

        cliente_email:
            E-mail único do cliente.

        tipo_solicitacao:
            Tipo de solicitação realizada pelo cliente.

        valor_patrimonio:
            Valor patrimonial informado pelo cliente.
    """

    __tablename__ = "customers"

    customer_id: Mapped[str] = mapped_column(
        primary_key=True,
        default=lambda: str(uuid4())
    )

    cliente_nome: Mapped[str] = mapped_column(
        nullable=False
    )

    prioridade: Mapped[Priority] = mapped_column(
        default=Priority.prioridade_normal
    )

    status: Mapped[str] = mapped_column(
        default="Aguardando Análise"
    )

    cliente_email: Mapped[str] = mapped_column(
        unique=True,
        nullable=False
    )

    tipo_solicitacao: Mapped[str] = mapped_column(
        nullable=False
    )

    valor_patrimonio: Mapped[int] = mapped_column(
        nullable=False
    )