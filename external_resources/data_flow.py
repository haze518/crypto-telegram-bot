from data_loader import AbstractDataLoader
from data_store import AbstractDataStore


class DataFlow:
    def __init__(self, loader: AbstractDataLoader, store: AbstractDataStore):
        self._loader = loader
        self._store = store

    async def load_and_save(self, aioht_session, motor_session, motor_client) -> None:
        data = await self._loader.load(aioht_session)
        await self._store.store(motor_session, motor_client, data)
