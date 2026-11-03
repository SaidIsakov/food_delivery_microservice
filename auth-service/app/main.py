from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_db, engine
from .schemas import TokenResponse, UserLogin, UserRead, UserRegister
from .models import User
from .security import create_access_token, verify_password
from .dependencies import get_auth_service
from .services import AuthService


@asynccontextmanager
async def lifespan(app: FastAPI):
  from .models import Base, User
  async with engine.begin() as database_session:
    await database_session.run_sync(Base.metadata.create_all)
  yield

app = FastAPI(lifespan=lifespan)

@app.post(
  '/register',
  response_model=TokenResponse,
  status_code=status.HTTP_201_CREATED
)
async def register(
    payload: UserRegister,
    auth_service: AuthService = Depends(get_auth_service)
) -> TokenResponse:
  new_user = await auth_service.register(email=payload.email, password=payload.password)

  return new_user


@app.post('/login', response_model=TokenResponse)
async def login(
  payload: UserLogin,
  auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
  return await auth_service.login(password=payload.password, email=payload.password)
