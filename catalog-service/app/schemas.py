from pydantic import BaseModel, Field, ConfigDict
import uuid

class Product(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  id: int
  category: str
  name: str
  price: float = Field(gt=0)
  stock: int = Field(ge=0)


class ProductCreate(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  category: str
  name: str
  price: float = Field(gt=0)
  stock: int = Field(ge=0)


class ProductRead(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  id: uuid.UUID
  name: str
  category: str
  price: float
  stock: int
