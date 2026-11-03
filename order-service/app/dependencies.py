from fastapi import Depends, Request
from aiokafka import AIOKafkaProducer
from sqlalchemy.orm import Session

from .service import OrderService
from .database import get_db

def get_kafka_producer(request: Request):
  producer: AIOKafkaProducer = request.app.state.kafka_producer

  return producer


def get_order_service(
  db: Session = Depends(get_db)
) -> OrderService:
  return OrderService(db)
