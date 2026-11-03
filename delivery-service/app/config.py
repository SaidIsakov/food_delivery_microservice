from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    database_url: str

    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672/"

settings = Settings()
