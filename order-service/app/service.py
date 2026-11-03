from fastapi import HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from aiokafka import AIOKafkaProducer
import httpx
from aio_pika.abc import AbstractExchange

from .schemas import OrderCreate
from .config import settings
from .models import Order, OrderItem
from .kafka import publish_kafka_event
from .rabbitmq import publish_json

class OrderService:
  def __init__(self, db: Session) -> None:
    self.db = db

  async def create(
      self,
      payload: OrderCreate,
      exchange: AbstractExchange,
      user_id: str,
      kafka_producer: AIOKafkaProducer,
  ):
    total_price = 0
    order_items_data = []
    quantity = []
    for item in payload.items:
      response =  httpx.get(f'{settings.CATALOG_URL}/products/{item.product_id}')
      if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Product not found")
      product = response.json()
      if item.quantity > product['stock']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product out of stock")
      order_items_data.append({
        "product_id": item.product_id,
        "product_name": product["name"],
        "price": product["price"],
        "quantity": item.quantity
      })
      total_price += product['price'] * item.quantity
      quantity.append(item.quantity)

    new_order = Order(address=payload.address, total_price=total_price, user_id=user_id)
    self.db.add(new_order)
    self.db.flush()

    new_order.items = [
      OrderItem(order_id=new_order.id, **item_data) for item_data in order_items_data
    ]


    self.db.commit()

    rabbitmq_event = {
      "order_id": str(new_order.id),
      "address": new_order.address,
      "total_price": new_order.total_price
    }

    await publish_json(exchange=exchange, data=rabbitmq_event)

    kafka_event = {
      "order_id": str(new_order.id),
      "total_price": total_price,
      "quantity": quantity,
      "created_at": new_order.created_at.isoformat()
    }

    await publish_kafka_event(
      producer=kafka_producer,
      topic=settings.KAFKA_ANALITIC_ORDER_TOPIC,
      event=kafka_event
      )

    return new_order


  def get_order(self, order_id):
    stmt = select(Order).where(Order.id == order_id).options(selectinload(Order.items))
    result = self.db.execute(stmt)
    order = result.scalar_one_or_none()
    if order is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order
