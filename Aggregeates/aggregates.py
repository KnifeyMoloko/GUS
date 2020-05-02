"""
Aggregates endpoint aggregates getters.
Author: Maciej Cisowski
"""
from requests import Response
from common.helpers import get_api_key
from Rest import client


def aggregates(language: str = None) -> Response:
    headers = {}
    if language:
        headers.update({"Accept-Language": language})
    data = client.get(resource_path="aggregates", headers=headers)
    return data
