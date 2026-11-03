from .schemas import ProductRead
from .models import Product

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

import uuid

class ProductService:
  def __init__(self, db: AsyncSession) -> None:
    self.db = db

  async def get_products(self) -> list[ProductRead]:
    stmt = select(Product)
    products = (await self.db.scalars(stmt)).all()
    return [ProductRead.model_validate(product) for product in products]

  async def get_product(self, product_id: uuid.UUID) -> ProductRead:
    product = await self.db.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductRead.model_validate(product)

