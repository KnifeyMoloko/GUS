from assertpy import assert_that, soft_assertions
from http import HTTPStatus
from Client.gus_rest_client import GUSClient


def test_rest_client_returns_ok(gus_client):
    request = gus_client.get(resource_path="", headers={})
    assert_that(request.status_code)\
        .is_equal_to(HTTPStatus.OK)
