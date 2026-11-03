from fastapi import APIRouter, status
import httpx
from fastapi.responses import JSONResponse

from app.config import settings


router = APIRouter(prefix='/catalog', tags=['catalog'])


@router.get('/api/v1/products', status_code=status.HTTP_200_OK)
async def get_products():
  async with httpx.AsyncClient() as client:
    response = await client.get(url=f"{settings.CATALOG_URL}/products")

    return JSONResponse(
      status_code=response.status_code,
      content=response.json()
    )


@router.get('/api/v1/products/{id}', status_code=status.HTTP_200_OK)
async def get_product(id: str):
  async with httpx.AsyncClient() as client:
    response = await client.get(url=f"{settings.CATALOG_URL}/products/{id}")

    return JSONResponse(
      status_code=response.status_code,
      content=response.json()
    )
