import aiohttp
import asyncio
import motor.motor_asyncio
import os
import time
from dataclasses import dataclass

from data_flow import DataFlow
from data_loader import GetParams, GetDataLoader
from data_store import MongoDataStore


@dataclass
class UriData:
    username: str
    password: str
    host: str
    port: int
    database: str


def _generate_uri(uri: UriData) -> str:
    return f"mongodb://{uri.username}:{uri.username}@{uri.host}:{uri.port}/{uri.database}?authSource=admin"


async def main():
    database = os.environ.get('MONGODB_DATABASE') or 'crypto_data'
    collection = os.environ.get('MONGODB_COLLECTION') or 'coingecko'
    uri_data = UriData(
        username=os.environ.get('MONGODB_USERNAME') or 'admin',
        password=os.environ.get('MONGODB_PASSWORD') or 'admin',
        host=os.environ.get('MONGODB_HOST') or 'localhost',
        port=os.environ.get('MONGODB_PORT') or 27017,
        database=database
    )
    flow = DataFlow(
        GetDataLoader(
            GetParams(
                url='https://api.coingecko.com/api/v3/coins/markets',
                params={'vs_currency': 'usd'},
            ),
        ),
        MongoDataStore(database=database, collection=collection),
    )
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                client = motor.motor_asyncio.AsyncIOMotorClient(_generate_uri(uri_data))
                await flow.load_and_save(session, client)
        except Exception:
            pass
        time.sleep(60)


if __name__ == '__main__':
    asyncio.run(main())
