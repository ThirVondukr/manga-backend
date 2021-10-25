import pytest

from gql.app import schema


@pytest.fixture(scope="session")
def gql_schema():
    return schema
