from fastapi import APIRouter

from app.api.v1.routers import customer, webhooks

router = APIRouter(tags=["v1", "API"])

router.include_router(customer.router, prefix="/clientes")
router.include_router(webhooks.router, prefix="/webhooks")

