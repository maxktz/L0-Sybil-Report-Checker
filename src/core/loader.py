from telethon import TelegramClient
from redis.asyncio import ConnectionPool, Redis
from yarl import URL
from src.github_client import GithubClient
from src.core.config import settings
import socks  # necessary package for telethon proxy work

redis_client = Redis(
    connection_pool=ConnectionPool(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD,
        db=settings.REDIS_DB,
    ),
)

telethon_proxy = settings.TELEGRAM_PROXY
if telethon_proxy:
    proxy_url = URL(str(telethon_proxy))
    telethon_proxy = {
        "proxy_type": proxy_url.scheme,
        "username": proxy_url.user,
        "password": proxy_url.password,
        "addr": proxy_url.host,
        "port": proxy_url.port,
    }
telegram_client = TelegramClient(
    session=settings.TELEGRAM_SESSION,
    api_id=settings.TELEGRAM_API_ID,
    api_hash=settings.TELEGRAM_API_HASH,
    proxy=telethon_proxy,
    device_model=settings.TELEGRAM_DEVICE_MODEL,
    system_version=settings.TELEGRAM_SYSTEM_VERSION,
    app_version=settings.TELEGRAM_APP_VERSION,
)

github_client = GithubClient(
    user_agent=settings.GITHUB_USER_AGENT,
    auth_token=settings.GITHUB_ACCESS_TOKEN,
)
