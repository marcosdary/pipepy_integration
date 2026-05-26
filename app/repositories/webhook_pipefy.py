from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# Models
from app.models import WebhookPipefyModel

# Schemas
from app.schemas.customer import (
    CustomerCreateSchema,
    CustomerUpdateSchema
)

from app.core.constants import Status

# Exceptions
from app.exceptions import ForbiddenActionError

class WebhookPipefyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self, event_id: str, status: Status
    ) -> WebhookPipefyModel: 
        webhook_pipefy = WebhookPipefyModel(event_id=event_id, status=status)
        self.session.add(webhook_pipefy)
        return webhook_pipefy
    
    async def get_by_id(
        self, 
        event_id: str
    ) -> None:
        query = select(WebhookPipefyModel).where(
            WebhookPipefyModel.event_id == event_id
        )

        webhook_pipefy = await self.session.scalar(query)
        if not webhook_pipefy:
            return
        
        if webhook_pipefy.status == Status.processed:
            raise ForbiddenActionError("Evento já processado")
        