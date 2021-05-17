from data_loader import AbstractDataLoader
from data_store import AbstractDataStore


class DataFlow:
    def __init__(self, loader: AbstractDataLoader, store: AbstractDataStore):
        self._loader = loader
        self._store = store

    async def load_and_save(self, client_session, client_store) -> None:
        data = await self._loader.load(client_session)
        self._store = await self._store.store(client_store, data)
