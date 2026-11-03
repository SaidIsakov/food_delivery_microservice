from fastapi import Depends
from .database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from .service import ProductService


def get_product_service(
  db: AsyncSession = Depends(get_db)
) -> ProductService:
  return ProductService(db)
