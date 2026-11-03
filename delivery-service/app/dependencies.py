from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .service import DelivereService
from .database import get_db

def get_delivery_service(
  db: AsyncSession = Depends(get_db)
) -> DelivereService:
  return DelivereService(db)
