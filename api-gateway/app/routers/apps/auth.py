from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
import httpx

from app.schemas import UserLogin, UserRegister
from app.config import settings
from app.auth import CurrentUser, get_current_user


router = APIRouter(prefix='/aith', tags=['auth'])


@router.post('/register')
async def register(
  payload: UserRegister
):
  async with httpx.AsyncClient() as client:
    response = await client.post(url=f"{settings.AUTH_URL}/register", json=payload.model_dump(mode="json"))
    return JSONResponse(
        status_code=response.status_code,
        content=response.json()
    )



@router.post('/login')
async def login(
  payload: UserLogin
):
  async with httpx.AsyncClient() as client:
    response = await client.post(url=f"{settings.AUTH_URL}/login", json=payload.model_dump(mode="json"))
    return JSONResponse(
        status_code=response.status_code,
        content=response.json()
    )


@router.get('/me', response_model=CurrentUser)
async def get_me(current_user = Depends(get_current_user)):
  return current_user
