from fastapi import APIRouter

from app.api.v1.routers import customer, webhooks

# Router principal da versão v1 da API
router = APIRouter()

# Rotas relacionadas aos clientes
router.include_router(
    customer.router,
    prefix="/clientes"
)

# Rotas relacionadas aos webhooks
router.include_router(
    webhooks.router,
    prefix="/webhooks"
)