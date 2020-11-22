import pytest
from clients.gus_rest_client import GUSClient
from common.helpers import get_api_key


@pytest.fixture
def gus_client():
    return GUSClient(api_key=get_api_key(), ssl=True)
