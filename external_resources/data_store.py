import logging
from abc import ABC, abstractmethod
import motor.motor_asyncio


class AbstractDataStore(ABC):
    @abstractmethod
    async def store(self):
        """Сохранить данные в хранилище."""


class MongoDataStore(AbstractDataStore):

    async def store(self, session, collection, data):
        try:
            await collection.insert_many(data, session=session)
        except Exception:
            logging.debug(data)
