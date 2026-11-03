from contextlib import asynccontextmanager
import uuid
from fastapi import FastAPI, status, Depends

from .rabbitmq import connect_rabbitmq, declare_orders_exchange
from .consumer import start_delivery_consumer
from .database import engine
from .schemas import DeliveryRead, DeliveryUpdate
from .dependencies import get_delivery_service
from .service import DelivereService

@asynccontextmanager
async def lifespan(app: FastAPI):
  from .models import Base, Delivery
  async with engine.begin() as database_connection:
    await database_connection.run_sync(Base.metadata.create_all)

  connection = await connect_rabbitmq()
  channel = await connection.channel()
  await declare_orders_exchange(channel=channel)
  await start_delivery_consumer(connection=connection)

  try:
    yield
  finally:
    await connection.close()

app = FastAPI(lifespan=lifespan)


@app.get('/deliveries', status_code=status.HTTP_200_OK, response_model=list[DeliveryRead])
async def get_deliveries(
  delivery_service: DelivereService = Depends(get_delivery_service)
) -> list[DeliveryRead]:
  deliveries = await delivery_service.get_all()
  return deliveries


@app.patch('/deliveries/{delivery_id}', status_code=status.HTTP_200_OK, response_model=DeliveryRead)
async def update_delivery(
  delivery_id: uuid.UUID,
  payload: DeliveryUpdate,
  delivery_service: DelivereService = Depends(get_delivery_service),
) -> DeliveryRead:
  return await delivery_service.update_delivery(delivery_id=delivery_id, payload=payload)
