import pytest
import os
from Rest.GUSRestClient import GUSClient
from common.helpers import get_api_key


@pytest.fixture
def gus_rest_client():
    return GUSClient(api_key=get_api_key(),
                     ssl=True)

