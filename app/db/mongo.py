from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import get_settings

settings = get_settings()


class MongoDB:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient | None = None
        self.database: AsyncIOMotorDatabase | None = None

    async def connect(self) -> None:
        self.client = AsyncIOMotorClient(settings.mongodb_uri)
        self.database = self.client[settings.mongodb_db_name]

        # Force a connection check instead of waiting for the first query.
        await self.client.admin.command("ping")

    async def disconnect(self) -> None:
        if self.client is not None:
            self.client.close()

        self.client = None
        self.database = None

    def get_database(self) -> AsyncIOMotorDatabase:
        if self.database is None:
            raise RuntimeError("MongoDB connection has not been initialized.")

        return self.database


mongodb = MongoDB()