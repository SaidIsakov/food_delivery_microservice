import json

import aio_pika
from aio_pika.abc import AbstractChannel, AbstractQueue, AbstractExchange

from .config import settings


async def connect_rabbitmq():
  return await aio_pika.connect_robust(settings.RABBITMQ_URL)


async def declare_orders_exchange(channel: AbstractChannel):
  return await channel.declare_exchange(
    "order"
  )


async def publish_json(exchange: AbstractExchange, data):
  message = aio_pika.Message(json.dumps(data).encode())
  await exchange.publish(message=message, routing_key='order.created')
