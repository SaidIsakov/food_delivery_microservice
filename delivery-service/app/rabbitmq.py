import aio_pika
from aio_pika.abc import AbstractChannel, AbstractQueue, AbstractExchange

from .config import settings


async def connect_rabbitmq():
  return await aio_pika.connect_robust(settings.RABBITMQ_URL)


async def declare_orders_exchange(channel: AbstractChannel):
  return await channel.declare_exchange(
    "order"
  )

async def declare_delivery_queue(channel: AbstractChannel, exchange: AbstractExchange):
  queue: AbstractQueue = await channel.declare_queue(
    "delivery.order_created"
  )
  await queue.bind(exchange,routing_key='order.created')
  return queue
