from pydantic_settings import BaseSettings, SettingsConfigDict

from typing import Optional

_base_config = SettingsConfigDict(
    env_file="./.env",
    env_ignore_empty=True,
    extra="ignore",
)
class DatabaseSettings(BaseSettings):
    POSTGRES_SERVER: Optional[str] = None
    POSTGRES_PORT: Optional[int] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None

    REDIS_HOST: Optional[str] = None
    REDIS_PORT: Optional[int] = None
    model_config = _base_config
    @property
    def POSTGRES_URL(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


class SecuritySettings(BaseSettings):

    JWT_SECRET: str = "your_default_jwt_secret"
    JWT_ALGORITHM: str = "HS256"
    model_config = _base_config


db_settings = DatabaseSettings()
#print("Using database URL:", db_settings.POSTGRES_URL)
security_settings = SecuritySettings()
#print(f"Connected to Redis at {db_settings.REDIS_HOST}:{db_settings.REDIS_PORT}")