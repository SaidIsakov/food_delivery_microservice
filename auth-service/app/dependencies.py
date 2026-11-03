from fastapi import Depends
from .database import get_db
from .services import AuthService
from sqlalchemy.ext.asyncio import AsyncSession

def get_auth_service(
  db: AsyncSession = Depends(get_db),
) -> AuthService:
  return AuthService(db)
