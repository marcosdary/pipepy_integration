from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# Models
from app.models import CustomerModel

# Schemas
from app.schemas.customer import (
    CustomerCreateSchema,
    CustomerUpdateSchema
)

from app.core.constants import Priority

# Exceptions
from app.exceptions import NotFoundError, DuplicateReviewError

class CustomerRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self, schema: CustomerCreateSchema
    ) -> CustomerModel: 
        
        query = await self.session.execute(
            select(CustomerModel.cliente_email).where(CustomerModel.cliente_email == schema.cliente_email)
        )

        email_exists = query.first()

        if email_exists:
            raise DuplicateReviewError("Email está em uso.")

        customer = CustomerModel(**schema.model_dump())
        self.session.add(customer)
        return customer
    
    async def update(
        self, 
        schema: CustomerUpdateSchema
    ) -> CustomerModel:
        query = select(CustomerModel).where(
            CustomerModel.cliente_email == schema.cliente_email
        )

        customer = await self.session.scalar(query)
        if not customer:
            raise NotFoundError("Cliente não encontrado")
        
        prioridade = Priority.prioridade_normal

        if customer.valor_patrimonio >= 200_000:
            prioridade = Priority.prioridade_alta

        schema.prioridade = prioridade
        
        for key, value in schema.model_dump().items():
            if value is not None:
                setattr(customer, key, value)

        return customer