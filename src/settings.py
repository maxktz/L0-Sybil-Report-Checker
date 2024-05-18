from pathlib import Path
from typing import Optional

from pydantic import MongoDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self

BOT_DIR = Path(__file__).absolute().parent.parent
ROOT_DIR = BOT_DIR.parent
LOCALES_DIR = BOT_DIR / "translations"
I18N_DOMAIN = "messages"
DEFAULT_LANGUAGE_CODE = "ru"


class EnvBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
        env_file_encoding="utf-8",
    )


class CacheSettings(EnvBaseSettings):
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None


class Settings(CacheSettings):
    GITHUB_ACCESS_TOKEN: str
    MONGODB_DSN: str
    GITHUB_USER_AGENT: str = "PostmanRuntime/7.37.3"
    DEBUG_MODE: bool = False


settings = Settings()
