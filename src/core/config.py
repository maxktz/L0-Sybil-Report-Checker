from pathlib import Path
from typing import Optional

from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).absolute().parents[2]


class EnvBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
        env_file_encoding="utf-8",
    )


class RedisSettings(EnvBaseSettings):
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None


class TelegramSettings(EnvBaseSettings):
    TELEGRAM_SESSION: Path = ROOT_DIR / "account"
    TELEGRAM_PROXY: Optional[str] = None
    """str, 'protocol://user:password@host:port' """
    TELEGRAM_API_ID: int = 2040  # default of telegram desktop
    TELEGRAM_API_HASH: str = "b18441a1ff607e10a989891a5462e627"  # default of telegram desktop
    TELEGRAM_DEVICE_MODEL: str = "MacBook Air M1"
    TELEGRAM_SYSTEM_VERSION: str = "macOS 14.4.1"
    TELEGRAM_APP_VERSION: str = "4.16.8 arm64"


class Settings(RedisSettings, TelegramSettings):
    CHAT_ID_TO_SEND: int
    GITHUB_ACCESS_TOKEN: str
    GITHUB_USER_AGENT: str = "PostmanRuntime/7.37.3"


settings = Settings()
