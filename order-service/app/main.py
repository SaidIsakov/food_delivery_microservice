from contextlib import asynccontextmanager
import uuid
from fastapi import FastAPI, Header, Request, Depends
from fastapi import status
from sqlalchemy.orm import selectinload, Session
from sqlalchemy import select
from aiokafka import AIOKafkaProducer

from .schemas import OrderCreate, OrderRead
from .rabbitmq import connect_rabbitmq, declare_orders_exchange
from .database import engine
from .kafka import create_kafka_producer
from .dependencies import get_kafka_producer, get_order_service
from .service import OrderService


@asynccontextmanager
async def lifespan(app: FastAPI):
  from .models import Base, Order, OrderItem
  Base.metadata.create_all(bind=engine)
  rabbitmq_connection = await connect_rabbitmq()
  channel = await rabbitmq_connection.channel()
  orders_exchange = await declare_orders_exchange(channel=channel)
  app.state.orders_exchange = orders_exchange

  app.state.kafka_producer = await create_kafka_producer()
  await app.state.kafka_producer.start()
  try:
    yield
  finally:
    await rabbitmq_connection.close()
    await app.state.kafka_producer.stop()


app = FastAPI(lifespan=lifespan)



@app.post('/orders', status_code=status.HTTP_201_CREATED, response_model=OrderRead)
async def create_order(
  request: Request,
  payload: OrderCreate,
  user_id: str = Header(alias="X-User-Id"),
  order_service: OrderService = Depends(get_order_service),
  kafka_producer: AIOKafkaProducer=Depends(get_kafka_producer)
):
  order = await order_service.create(
    payload=payload,
    exchange=request.app.state.orders_exchange,
    user_id=user_id,
    kafka_producer=kafka_producer
  )

  return order


@app.get('/orders/{order_id}', status_code=status.HTTP_200_OK, response_model=OrderRead)
def get_order(
  order_id: uuid.UUID,
  order_service: OrderService = Depends(get_order_service),
):
  order = order_service.get_order(order_id=order_id)
  return order
