import asyncio
import aiohttp
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class GetParams:
    url: str
    params: dict = field(default_factory=dict)


class AbstractDataLoader(ABC):
    @abstractmethod
    async def load(self):
        """Выгрузка данных из источника."""


class GetDataLoader(AbstractDataLoader):

    def __init__(self, get_params: GetParams):
        self._get_params = get_params

    async def load(self, session: aiohttp.ClientSession) -> Optional[dict]:
        try:
            result = await session.get(url=self._get_params.url, params=self._get_params.params)
        except asyncio.TimeoutError:
            logging.debug(f'Error occured while load data from: {self._url}')
        else:
            if result.status != 200:
                logging.debug(f'error: server returned: {result.status}')
            return await result.json()
