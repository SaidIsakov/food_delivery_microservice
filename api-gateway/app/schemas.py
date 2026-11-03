import uuid

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class OrderItemCreate(BaseModel):
  product_id: uuid.UUID
  quantity: int



class OrderCreate(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  items: list[OrderItemCreate]
  address: str


class UserRead(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  id: str
  email: EmailStr



class TokenResponse(BaseModel):
  access_token: str
  user: UserRead


class CredentialsBase(BaseModel):
  email: EmailStr
  password: str = Field(max_length=128, min_length=8)

class UserRegister(CredentialsBase):
  pass

class UserLogin(CredentialsBase):
  pass
