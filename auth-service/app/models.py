from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from uuid import uuid4

class Base(DeclarativeBase):
  pass

class User(Base):
  __tablename__ = 'users'

  id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
  email: Mapped[str] = mapped_column(unique=True)
  password_hash: Mapped[str]
  created_at: Mapped[datetime] = mapped_column(
    default=datetime.now
  )




