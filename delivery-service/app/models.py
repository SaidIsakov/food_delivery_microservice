from datetime import datetime
import uuid

from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

class Base(DeclarativeBase):
  pass


class Delivery(Base):
  __tablename__ = 'deliveries'

  id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

  order_id: Mapped[uuid.UUID] = mapped_column(unique=True)
  address: Mapped[str]
  total_price: Mapped[float]
  status: Mapped[str] = mapped_column(default="new")
  courier_name: Mapped[str | None] = mapped_column(nullable=True)
  created_at: Mapped[datetime] = mapped_column(default=datetime.now)
