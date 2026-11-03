from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  model_config = SettingsConfigDict(env_file='.env', extra='ignore')

  database_url: str

  CATALOG_URL: str = "http://127.0.0.1:8000"
  RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672/"
  KAFKA_BOOTSTRAP_SERVER: str = 'kafka:9092'
  KAFKA_ANALITIC_ORDER_TOPIC: str = 'order-events'

settings = Settings()
