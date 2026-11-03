from aio_pika.abc import  AbstractRobustConnection
import json

from .rabbitmq import declare_orders_exchange, declare_delivery_queue
from .models import Delivery
from .database import Sessionlocal

async def process_order(message):
  async with message.process():
    data = json.loads(message.body.decode())
    async with Sessionlocal() as session:
      delivery = Delivery(
      order_id=str(data['order_id']),
      address=str(data['address']),
      total_price=data['total_price']
      )
      session.add(delivery)
      await session.commit()



async def start_delivery_consumer(connection: AbstractRobustConnection):
  channel = await connection.channel()
  orders_exchange = await declare_orders_exchange(channel=channel)
  queue = await declare_delivery_queue(channel=channel, exchange=orders_exchange)

  await queue.consume(callback=process_order)
