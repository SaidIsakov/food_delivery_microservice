import json
from pymongo.collection import Collection
from aiokafka import AIOKafkaConsumer, ConsumerRecord

from .coonfig import settings


async def save_event(collection: Collection, message: ConsumerRecord):
  event = json.loads(message.value)
  await collection.insert_one(event)


async def consume_events(collection: Collection):
  consumer = AIOKafkaConsumer(
    settings.KAFKA_ANALITIC_ORDER_TOPIC,
    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVER
  )

  await consumer.start()

  try:
    async for message in consumer:
      await save_event(collection, message)
  finally:
    await consumer.stop()
