from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Core
from app.core.constants import Status

# Exceptions
from app.exceptions import ForbiddenActionError

# Models
from app.models import WebhookPipefyModel


class WebhookPipefyRepository:
    """
    Repositório responsável pelas operações
    relacionadas aos webhooks do Pipefy.

    Attributes:
        session:
            Sessão assíncrona do banco de dados.
    """

    def __init__(self, session: AsyncSession):
        """
        Inicializa o repositório de webhooks.

        Args:
            session:
                Sessão assíncrona do SQLAlchemy.
        """
        self.session = session

    async def create(
        self,
        event_id: str,
        status: Status
    ) -> WebhookPipefyModel:
        """
        Cria um registro de webhook processado.

        Args:
            event_id:
                Identificador do evento recebido.

            status:
                Status do processamento do webhook.

        Returns:
            WebhookPipefyModel:
                Instância do webhook criada.
        """

        # Cria a entidade do webhook
        webhook_pipefy = WebhookPipefyModel(
            event_id=event_id,
            status=status
        )

        # Adiciona o webhook na sessão
        self.session.add(webhook_pipefy)

        return webhook_pipefy

    async def get_by_id(
        self,
        event_id: str
    ) -> None:
        """
        Verifica se um evento já foi processado.

        Caso o evento exista e já esteja com status
        processado, uma exceção será lançada.

        Args:
            event_id:
                Identificador do evento.

        Raises:
            ForbiddenActionError:
                Caso o evento já tenha sido processado.
        """

        # Busca o webhook pelo identificador do evento
        query = select(WebhookPipefyModel).where(
            WebhookPipefyModel.event_id == event_id
        )

        webhook_pipefy = await self.session.scalar(query)

        # Retorna caso o evento ainda não exista
        if not webhook_pipefy:
            return

        # Impede reprocessamento do evento
        if webhook_pipefy.status == Status.processed:
            raise ForbiddenActionError(
                "Evento já processado"
            )