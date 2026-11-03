import json

from aiokafka import AIOKafkaProducer

from .config import settings


async def create_kafka_producer():
  return AIOKafkaProducer(bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVER)


async def publish_kafka_event(producer: AIOKafkaProducer, topic: str, event: dict):
  return await producer.send_and_wait(topic, value=json.dumps(event).encode())
