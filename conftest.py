import pytest
from Client.gus_rest_client import GUSClient
from Common.helpers import get_api_key


@pytest.fixture
def gus_client():
    return GUSClient(api_key=get_api_key(), ssl=True)
