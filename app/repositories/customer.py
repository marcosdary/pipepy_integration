from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Core
from app.core.constants import Priority

# Exceptions
from app.exceptions import (
    DuplicateReviewError,
    NotFoundError
)

# Models
from app.models import CustomerModel

# Schemas
from app.schemas.customer import (
    CustomerCreateSchema,
    CustomerUpdateSchema
)


class CustomerRepository:
    """
    Repositório responsável pelas operações
    relacionadas aos clientes.

    Attributes:
        session:
            Sessão assíncrona do banco de dados.
    """

    def __init__(self, session: AsyncSession):
        """
        Inicializa o repositório de clientes.

        Args:
            session:
                Sessão assíncrona do SQLAlchemy.
        """
        self.session = session

    async def create(
        self,
        schema: CustomerCreateSchema
    ) -> CustomerModel:
        """
        Cria um novo cliente no banco de dados.

        Antes da criação, verifica se o e-mail
        já está sendo utilizado.

        Args:
            schema:
                Dados necessários para criação
                do cliente.

        Returns:
            CustomerModel:
                Instância do cliente criado.

        Raises:
            DuplicateReviewError:
                Caso o e-mail já esteja cadastrado.
        """

        # Busca um cliente com o mesmo e-mail
        query = await self.session.execute(
            select(CustomerModel.cliente_email).where(
                CustomerModel.cliente_email == schema.cliente_email
            )
        )

        email_exists = query.first()

        # Valida se o e-mail já está em uso
        if email_exists:
            raise DuplicateReviewError(
                "Email está em uso."
            )

        # Cria a entidade do cliente
        customer = CustomerModel(
            **schema.model_dump()
        )

        # Adiciona o cliente na sessão
        self.session.add(customer)

        return customer

    async def update(
        self,
        schema: CustomerUpdateSchema
    ) -> CustomerModel:
        """
        Atualiza os dados de um cliente.

        A prioridade do cliente é recalculada
        com base no valor do patrimônio.

        Args:
            schema:
                Dados utilizados para atualização
                do cliente.

        Returns:
            CustomerModel:
                Cliente atualizado.

        Raises:
            NotFoundError:
                Caso o cliente não seja encontrado.
        """

        # Busca o cliente pelo e-mail
        query = select(CustomerModel).where(
            CustomerModel.cliente_email == schema.cliente_email
        )

        customer = await self.session.scalar(query)

        # Valida se o cliente existe
        if not customer:
            raise NotFoundError(
                "Cliente não encontrado"
            )

        # Define prioridade padrão
        prioridade = Priority.prioridade_normal

        # Atualiza prioridade caso patrimônio seja alto
        if customer.valor_patrimonio >= 200_000:
            prioridade = Priority.prioridade_alta

        # Atualiza prioridade no schema
        schema.prioridade = prioridade

        # Atualiza dinamicamente os campos do cliente
        for key, value in schema.model_dump().items():
            if value is not None:
                setattr(customer, key, value)

        return customer