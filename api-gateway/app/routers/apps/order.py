from fastapi import APIRouter, Depends, status, HTTPException
import httpx
from fastapi.responses import JSONResponse

from app.schemas import OrderCreate
from app.auth import get_current_user, CurrentUser
from app.config import settings

router = APIRouter(prefix='/orders', tags=['orders'])


@router.post('/api/v1/orders', status_code=status.HTTP_201_CREATED)
async def create_order(payload: OrderCreate, current_user = Depends(get_current_user)):
  async with httpx.AsyncClient() as client:
    response = await client.post(
      url=f"{settings.ORDER_URL}/orders",
      json=payload.model_dump(mode="json"),
      headers={
        'X-User-Id': current_user.id
      }
    )

    return JSONResponse(
      status_code=response.status_code,
      content=response.json()
    )

@router.get('/api/v1/orders/{id}', status_code=status.HTTP_200_OK)
async def get_order(id: str, user: CurrentUser = Depends(get_current_user)):
  async with httpx.AsyncClient() as client:
    response = await client.get(url=f"{settings.ORDER_URL}/orders/{id}")
    response_data = response.json()
    ensure_order_owner(response_data, user)
    return JSONResponse(
      status_code=response.status_code,
      content=response_data
    )



def ensure_order_owner(order, user: CurrentUser) -> None:
  if not isinstance(order, dict) or order.get("user_id") != user.id:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Order not found"
    )
