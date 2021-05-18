import pytest

from data_flow import DataFlow
from data_store import MongoDataStore


class MockDataLoader:

    async def load(self, params):
        return params

# TODO не создается БД

@pytest.mark.parametrize(
    ('params', 'expected'),
    (
        ({'rings': 11}, {'rings': 11}),
    ),
)
async def test_data_flow(params, expected, mongo, loop):
    flow = DataFlow(
        MockDataLoader(),
        MongoDataStore(),
    )
    mongo_collection, mongo_session = mongo
    await flow.load_and_save(params, mongo_session, mongo_collection)
    result = await mongo_collection.find_one(expected)
    assert result == expected
