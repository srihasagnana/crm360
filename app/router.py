from fastapi import APIRouter
from app.routers.deal_router import router as deal_router
from app.routers.product_router import router as product_router
from app.routers.customer_router import router as customer_router
from app.routers.order_router import router as order_router
from app.routers.contact_router import router as contact_router
from app.routers.interactions_router import router as interactions_router
from app.routers.complaint_router import router as complaint_router

api_router = APIRouter(prefix="/api")

api_router.include_router(product_router, tags=["product"])
api_router.include_router(customer_router, tags=["customer"])
api_router.include_router(order_router, tags=["order"])
api_router.include_router(contact_router, tags=["contact"])
api_router.include_router(interactions_router, tags=["interaction"])
api_router.include_router(complaint_router, tags=["complaint"])
api_router.include_router(deal_router, tags=["deal"])