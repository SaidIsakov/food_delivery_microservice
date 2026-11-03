from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import status, HTTPException
import uuid

from .schemas import DeliveryRead, DeliveryUpdate
from .models import Delivery


class DelivereService:
  def __init__(self, db: AsyncSession) -> None:
    self.db = db

  async def get_all(self) -> list[DeliveryRead]:
    smtp = select(Delivery)
    deliveries = (await self.db.scalars(smtp)).all()

    return [DeliveryRead.model_validate(delivery) for delivery in deliveries]

  async def update_delivery(self, delivery_id: uuid.UUID, payload: DeliveryUpdate) -> DeliveryRead:
    delivery = await self.db.get(Delivery, delivery_id)
    if delivery:
      delivery.status = 'assigned'
      delivery.courier_name = payload.courier_name
      await self.db.commit()
      await self.db.refresh(delivery)
      return DeliveryRead.model_validate(delivery)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Delivery not found")

