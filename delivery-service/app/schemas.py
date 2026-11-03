from datetime import datetime
import uuid

from pydantic import BaseModel, ConfigDict


class DeliveryRead(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  id: uuid.UUID
  order_id: uuid.UUID
  address: str
  total_price: float
  status: str
  courier_name: str | None
  created_at: datetime


class DeliveryUpdate(BaseModel):
  model_config = ConfigDict(from_attributes=True)
  courier_name: str
