from sqlalchemy.orm import mapped_column, Mapped
from uuid import uuid4

from app.models.base import BaseModel
from app.core.constants import Priority

class CustomerModel(BaseModel):
    __tablename__ = "customers"
    customer_id: Mapped[str] = mapped_column(
        primary_key=True,
        default=lambda: str(uuid4())
    )
    cliente_nome: Mapped[str] = mapped_column(nullable=False)
    prioridade: Mapped[Priority] = mapped_column(default=Priority.prioridade_normal)
    status: Mapped[str] = mapped_column(default="Aguardando Análise")
    cliente_email: Mapped[str] = mapped_column(unique=True, nullable=False)
    tipo_solicitacao: Mapped[str] = mapped_column(nullable=False)
    valor_patrimonio: Mapped[int] = mapped_column(nullable=False)

