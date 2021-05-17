import logging
from abc import ABC, abstractmethod
import motor.motor_asyncio


class AbstractDataStore(ABC):
    @abstractmethod
    async def store(self):
        """Сохранить данные в хранилище."""


class MongoDataStore(AbstractDataStore):

    def __init__(self, database: str, collection: str):
        self._database = database
        self._collection = collection

    async def store(self, client: motor.motor_asyncio.AsyncIOMotorClient, data: dict):
        collection = client[self._database][self._collection]
        async with await client.start_session() as s:
            try:
                await collection.insert_many(data, session=s)
            except Exception:
                logging.debug(data)
