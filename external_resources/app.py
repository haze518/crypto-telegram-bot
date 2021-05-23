import aiohttp
import asyncio
import motor.motor_asyncio
import os
import time

from data_flow import DataFlow
from data_loader import GetParams, GetDataLoader
from data_store import MongoDataStore


database = os.environ.get('MONGODB_DATABASE') or 'crypto_data'
collection = os.environ.get('MONGODB_COLLECTION') or 'coingecko'
username=os.environ.get('MONGODB_USERNAME') or 'admin'
password=os.environ.get('MONGODB_PASSWORD') or 'admin'
host=os.environ.get('MONGODB_HOST') or 'localhost'
port=os.environ.get('MONGODB_PORT') or 27017


def _generate_uri(username, password, host, port, database) -> str:
    return f"mongodb://{username}:{password}@{host}:{port}/{database}?authSource=admin"


async def main():

    config = {
        'database': database,
        'username': username,
        'password': password,
        'host': host,
        'port': port,
    }

    flow = DataFlow(
        GetDataLoader(
            GetParams(
                url='https://api.coingecko.com/api/v3/coins/markets',
                params={'vs_currency': 'usd'},
            ),
        ),
        MongoDataStore(),
    )

    motor_client = motor.motor_asyncio.AsyncIOMotorClient(_generate_uri(**config))
    motor_collection = motor_client[database][collection]
    while True:
        async with aiohttp.ClientSession() as aio_session:
            async with await motor_client.start_session() as motor_session:
                await flow.load_and_save(aio_session, motor_session, motor_collection)
        time.sleep(60*10)


if __name__ == '__main__':
    asyncio.run(main())
