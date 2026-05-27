from uuid import uuid4

from sqlalchemy.orm import Mapped, mapped_column

from app.core.constants import Status
from app.models.base import BaseModel


class WebhookPipefyModel(BaseModel):
    """
    Modelo responsável por armazenar os eventos
    recebidos via webhook do Pipefy.

    Attributes:
        event_id:
            Identificador único do evento do webhook.

        status:
            Status atual do processamento do webhook.
    """

    __tablename__ = "webhook_pipefy"

    event_id: Mapped[str] = mapped_column(
        primary_key=True,
        default=lambda: str(uuid4())
    )

    status: Mapped[Status] = mapped_column(
        default=Status.pending
    )