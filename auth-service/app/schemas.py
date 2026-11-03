from pydantic import BaseModel, Field, ConfigDict, EmailStr

class CredentialsBase(BaseModel):
  email: EmailStr
  password: str = Field(max_length=128, min_length=8)

class UserRegister(CredentialsBase):
  pass

class UserLogin(CredentialsBase):
  pass

class UserRead(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  id: str
  email: EmailStr


class TokenResponse(BaseModel):
  access_token: str
  user: UserRead
