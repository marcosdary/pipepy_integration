from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

# Repositories
from app.repositories import CustomerRepository

# Core
from app.core.config import get_session

# Schemas
from app.schemas.customer import (
    CustomerCreateSchema,
    CustomerReadSchema
)
from app.schemas.pipefy.card import (
    PipefyCardCreateSchema
)
from app.schemas.pipefy.field import (
    PipefyFieldCreateSchema
)

# Services
from app.services import PipefyService

# Exceptions
from app.exceptions import DuplicateReviewError, UnprocessableEntity

router = APIRouter()

@router.post(
    "", 
    status_code=status.HTTP_201_CREATED, 
    response_model=CustomerReadSchema,
    summary="Criar cliente",
    description="Cria cliente e sincroniza com Pipefy.",
    responses={
        409: {"description": "Cliente duplicado"},
        422: {"description": "Erro de validação"},
        500: {"description": "Erro interno"},
    }
)
async def create_customer(
    customer: CustomerCreateSchema, 
    session: AsyncSession = Depends(get_session)
):
    try:
        customer_repo = CustomerRepository(session)
        
        fields_attributes = [
            PipefyFieldCreateSchema(field_id=key, field_value=str(value))
            for key, value in customer.model_dump().items()
        ]
        schema = PipefyCardCreateSchema(
            title=customer.cliente_nome,
            fields_attributes=fields_attributes
        )
        response = await customer_repo.create(customer)

        pipefy_service = PipefyService()
        
        await session.commit()
        await pipefy_service.create_card(schema)
        return CustomerReadSchema.model_validate(response)
    
    except DuplicateReviewError as exc:
        await session.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail=str(exc)
        )
    
    except UnprocessableEntity as exc:
        await session.rollback()
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(exc)
        )

    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="Cliente já cadastrado."
        )

    except Exception as exc:
        await session.rollback()
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno do servidor: {str(exc)}"    
        )
