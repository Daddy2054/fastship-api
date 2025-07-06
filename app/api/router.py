from fastapi import APIRouter

from app.api.routers import delivery_partner
from .routers import shipment, seller

# Single router to group all api routers
master_router = APIRouter()

master_router.include_router(shipment.router)
master_router.include_router(seller.router)
master_router.include_router(delivery_partner.router)
