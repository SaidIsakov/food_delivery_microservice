from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
  model_config = SettingsConfigDict(env_file='.env', extra='ignore')

  jwt_secret: SecretStr
  jwt_algoritm: str = 'HS256'

  AUTH_URL: str = "http://127.0.0.1:8007"
  CATALOG_URL: str = "http://127.0.0.1:8000"
  ORDER_URL: str = "http://127.0.0.1:8001"

settings = Settings()
