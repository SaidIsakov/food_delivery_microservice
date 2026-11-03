from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  model_config = SettingsConfigDict(env_file='.env', extra='ignore')

  MONGODB_URL : str = (
    "mongodb://analytics:analytics@localhost:27017/analytics"
  )
  MONGODB_DATABASE: str = "analytics"
  MONGODB_COLLECTION: str = "events"

  KAFKA_BOOTSTRAP_SERVER: str = 'kafka:9092'
  KAFKA_ANALITIC_ORDER_TOPIC: str = 'order-events'

settings = Settings()
