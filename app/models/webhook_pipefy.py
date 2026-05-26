from sqlalchemy.orm import mapped_column, Mapped
from uuid import uuid4

from app.models.base import BaseModel
from app.core.constants import Status


class WebhookPipefyModel(BaseModel):
    __tablename__ = "webhook_pipefy"
    event_id: Mapped[str] = mapped_column(
        primary_key=True,
        default=lambda: str(uuid4())
    )
    status: Mapped[Status] = mapped_column(default=Status.pending)


