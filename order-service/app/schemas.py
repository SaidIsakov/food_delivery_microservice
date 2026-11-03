from datetime import datetime
import uuid

from pydantic import BaseModel, ConfigDict


class OrderItemCreate(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  product_id: uuid.UUID
  quantity: int



class OrderCreate(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  items: list[OrderItemCreate]
  address: str


class OrderRead(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  id: uuid.UUID
  status: str
  total_price: float
  address: str
  created_at: datetime
  items: list["OrderItem"]
  user_id: uuid.UUID

class OrderItem(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  id: uuid.UUID
  order_id: uuid.UUID
  product_id: uuid.UUID
  product_name: str
  price: float
  quantity: int
