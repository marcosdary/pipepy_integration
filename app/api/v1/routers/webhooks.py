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

router = APIRouter(tags=["webhook"])


@router.post(
    "/pipefy/card-updated",
    status_code=status.HTTP_201_CREATED
)
async def card_updated(
    pipefy: PipefyCardUpdatedWebhookSchema,
    session: AsyncSession = Depends(get_session)
) -> None:
    """
    Processa o webhook de atualização de card do Pipefy.

    Fluxo:
        1. Verifica se o evento já foi processado.
        2. Atualiza os dados do cliente.
        3. Atualiza os campos do card no Pipefy.
        4. Registra o webhook como processado.
        5. Confirma a transação no banco.

    Args:
        pipefy:
            Payload recebido do webhook do Pipefy.

        session:
            Sessão assíncrona do banco de dados.

    Returns:
        dict:
            Resultado do processamento do webhook.

    Raises:
        HTTPException:
            - 404: Recurso não encontrado.
            - 403: Ação não permitida.
            - 500: Erro interno inesperado.
    """
    try:
        # Inicializa os repositórios
        webhook_pipefy_repo = WebhookPipefyRepository(session)
        customer_repo = CustomerRepository(session)

        # Verifica se o evento já foi processado
        await webhook_pipefy_repo.get_by_id(pipefy.event_id)

        # Atualiza os dados do cliente
        customer = await customer_repo.update(
            CustomerUpdateSchema(
                cliente_email=pipefy.cliente_email
            )
        )

        # Inicializa o serviço do Pipefy
        pipefy_service = PipefyService()

        # Atualiza os campos do card
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

        # Registra o webhook como processado
        await webhook_pipefy_repo.create(
            event_id=pipefy.event_id,
            status=Status.processed
        )

        # Confirma a transação
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