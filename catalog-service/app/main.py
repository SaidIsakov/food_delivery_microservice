from fastapi import FastAPI, Depends
from fastapi import status
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import ProductCreate, ProductRead
from .models import Product
from .database import engine, get_db
from .dependencies import get_product_service
from .service import ProductService

import uuid


@asynccontextmanager
async def lifespan(app: FastAPI):
  from .models import Product, Base
  async with engine.begin() as database_connection:
    await database_connection.run_sync(Base.metadata.create_all)
  yield

app = FastAPI(lifespan=lifespan)



@app.get(
  '/products',
  status_code=status.HTTP_200_OK, response_model=list[ProductRead])
async def get_products(product_service: ProductService = Depends(get_product_service)):
  products = await product_service.get_products()
  return products


@app.get('/products/{product_id}', status_code=status.HTTP_200_OK, response_model=ProductRead)
async def get_product(
  product_id: uuid.UUID,
  product_service: ProductService = Depends(get_product_service)
)-> ProductRead:
  product = await product_service.get_product(product_id=product_id)
  return product



@app.post('/products', status_code=status.HTTP_201_CREATED, response_model=ProductRead)
async def create_product(
  payload: ProductCreate,
  db: AsyncSession = Depends(get_db)
):
  product = Product(**payload.model_dump())
  db.add(product)
  await db.commit()
  await db.refresh(product)
  return product
