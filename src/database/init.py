from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from src.settings import settings

from .models import Report


async def init_db() -> None:
    await init_beanie(
        database=database,
        document_models=[],
    )


db_client = AsyncIOMotorClient(str(settings.MONGODB_DSN))
database = db_client.get_database()
