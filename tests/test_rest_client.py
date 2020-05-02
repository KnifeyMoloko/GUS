from assertpy import assert_that, soft_assertions
from http import HTTPStatus
from Rest.GUSRestClient import GUSClient


def test_rest_client_returns_ok(gus_rest_client):
    request = gus_rest_client.get(resource_path="",
                                  headers={})
    assert_that(request.status_code)\
        .is_equal_to(HTTPStatus.OK)
