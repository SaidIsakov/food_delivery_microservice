from fastapi import APIRouter
from .apps.auth import router as auth_router
from .apps.order import router as order_router
from .apps.catalog import router as catalog_router

router = APIRouter(prefix='/api')


router.include_router(auth_router)
router.include_router(order_router)
router.include_router(catalog_router)
