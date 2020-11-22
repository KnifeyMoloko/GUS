"""
Aggregates endpoint aggregates getters.
Author: Maciej Cisowski
"""
from requests import Response
from Common.helpers import get_api_key
from Client import client


def aggregates(language: str = None) -> Response:
    headers = {}
    if language:
        headers.update({"Accept-Language": language})
    data = client.get(resource_path="aggregates", headers=headers)
    return data
