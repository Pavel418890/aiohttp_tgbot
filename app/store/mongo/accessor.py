from typing import TYPE_CHECKING, Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, \
    AsyncIOMotorCollection

from app.base.base_accessor import BaseAccessor

if TYPE_CHECKING:
    from app.web.app import Application


class MongoAccessor(BaseAccessor):
    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.db: Optional[AsyncIOMotorDatabase] = None
        self.update_collection: Optional[AsyncIOMotorCollection] = None

    async def connect(self, app: "Application"):
        self.db = AsyncIOMotorClient(app.config.mongo.url).tgbot
        self.update_collection = self.db.updates
        self.app.logger.info("Connected to mongo db")
        
    async def insert_update_object(self, update_object: dict):
        result = await self.update_collection.insert_one(update_object)
        return result.inserted_id

