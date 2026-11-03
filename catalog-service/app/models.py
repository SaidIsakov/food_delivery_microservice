from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
import uuid


class Base(DeclarativeBase):
  pass

class Product(Base):
  __tablename__ = "products"
  
  id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
  name: Mapped[str]
  category: Mapped[str]
  price: Mapped[float]
  stock: Mapped[int]
