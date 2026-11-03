from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import uuid

class Base(DeclarativeBase):
  pass

class OrderItem(Base):
  __tablename__ = 'order_items'

  id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
  order_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('orders.id'))
  product_id: Mapped[uuid.UUID]
  product_name: Mapped[str]
  price: Mapped[float]
  quantity: Mapped[int]
  order: Mapped["Order"] = relationship(back_populates='items')


class Order(Base):
  __tablename__ = 'orders'

  id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
  status: Mapped[str] = mapped_column(default="new")
  total_price: Mapped[float]
  address: Mapped[str]
  created_at: Mapped[datetime] = mapped_column(default=datetime.now)
  items: Mapped[list[OrderItem]] = relationship(back_populates='order', cascade="all, delete-orphan")
  user_id: Mapped[uuid.UUID]
