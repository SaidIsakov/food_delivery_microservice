from .models import User
from .security import hash_password, create_access_token, verify_password
from .schemas import UserRegister, TokenResponse, UserRead

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import status
from fastapi import HTTPException



class AuthService:
  def __init__(self, db: AsyncSession) -> None:
    self.db = db

  async def register(self, email, password):
    new_user = User(email=email, password_hash=hash_password(password))
    self.db.add(new_user)
    await self.db.commit()
    await self.db.refresh(new_user)
    access_token = create_access_token(user=new_user)

    return TokenResponse(access_token=access_token, user=UserRead.model_validate(new_user))


  async def login(self, email, password):
    user = await self.db.scalar(select(User).where(User.email==str(email)))
    if user is not None:
      if not verify_password(password=password, encoded_password=user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
      access_token = create_access_token(user=user)
    return TokenResponse(
      access_token=access_token, user=UserRead.model_validate(user),
      )
