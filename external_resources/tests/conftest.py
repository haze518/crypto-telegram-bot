import asyncio
import pytest
import os
import motor.motor_asyncio

from app import _generate_uri


@pytest.fixture(scope='session')
def config():
    database = 'test_database'
    username=os.environ.get('MONGODB_USERNAME') or 'admin'
    password=os.environ.get('MONGODB_PASSWORD') or 'admin'
    host=os.environ.get('MONGODB_HOST') or 'localhost'
    port=os.environ.get('MONGODB_PORT') or 27017
    return {
        'database': database,
        'username': username,
        'password': password,
        'host': host,
        'port': port,
    }


def loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture
async def mongo(config, loop):
    collection = 'test_collection'
    client = motor.motor_asyncio.AsyncIOMotorClient(_generate_uri(**config))
    collection = client[config['database']][collection]
    async with await client.start_session() as session:
        yield collection, session
    await client.drop_database(config['database'])
