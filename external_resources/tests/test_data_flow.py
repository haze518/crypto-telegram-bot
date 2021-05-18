import pytest

from data_flow import DataFlow
from data_store import MongoDataStore


class MockDataLoader:

    async def load(self, params):
        return params


@pytest.mark.parametrize(
    ('params', 'expected'),
    (
        (
            [
                {'rings': 11},
            ],
            {'rings': 11},
        ),
        (
            None,
            None,
        )
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
    if isinstance(result, dict):
        assert all(item in result.items() for item in expected.items())
    else:
        assert result == expected
