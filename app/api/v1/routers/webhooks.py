from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

# Repositories
from app.repositories import CustomerRepository, WebhookPipefyRepository

# Core
from app.core.config import get_session
from app.core.constants import Status

# Service
from app.services import PipefyService

# Schemas
from app.schemas.customer import CustomerUpdateSchema
from app.schemas.pipefy.card import PipefyCardUpdatedWebhookSchema
from app.schemas.pipefy.field import PipefyFieldUpdateSchema

# Exceptions
from app.exceptions import ForbiddenActionError, NotFoundError

router = APIRouter()

@router.post(
    "/pipefy/card-updated",
    status_code=status.HTTP_201_CREATED,
    summary="Processa webhook de atualização de card do Pipefy",
    description="""
Processa eventos de atualização de card recebidos do Pipefy.

Fluxo do endpoint:
- Verifica se o evento já foi processado
- Atualiza dados do cliente no banco
- Sincroniza campos no Pipefy
- Registra o webhook como processado
- Confirma a transação no banco
""",
    responses={
        201: {
            "description": "Webhook processado com sucesso"
        },
        404: {
            "description": "Recurso não encontrado (cliente ou evento)"
        },
        403: {
            "description": "Ação não permitida"
        },
        500: {
            "description": "Erro interno inesperado"
        },
    },
)
async def card_updated(
    pipefy: PipefyCardUpdatedWebhookSchema,
    session: AsyncSession = Depends(get_session)
) -> dict:
    """
    Processa webhook de atualização de card do Pipefy.
    """
    try:
        webhook_pipefy_repo = WebhookPipefyRepository(session)
        customer_repo = CustomerRepository(session)

        await webhook_pipefy_repo.get_by_id(pipefy.event_id)

        customer = await customer_repo.update(
            CustomerUpdateSchema(
                cliente_email=pipefy.cliente_email
            )
        )

        pipefy_service = PipefyService()

        await pipefy_service.update_card_field(
            status=PipefyFieldUpdateSchema(
                card_id=pipefy.card_id,
                field_id="status",
                new_value=customer.status
            ),
            prioridade=PipefyFieldUpdateSchema(
                card_id=pipefy.card_id,
                field_id="prioridade",
                new_value=customer.prioridade
            )
        )

        await webhook_pipefy_repo.create(
            event_id=pipefy.event_id,
            status=Status.processed
        )

        await session.commit()

        return {
            "message": "Concluído com sucesso.",
            "event_id": pipefy.event_id,
            "ignored": False,
        }

    except NotFoundError as exc:
        await session.rollback()
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=str(exc)
        )

    except ForbiddenActionError as exc:
        await session.rollback()
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            detail=str(exc)
        )

    except Exception as exc:
        await session.rollback()
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc)
        )