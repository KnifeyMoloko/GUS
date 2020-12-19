"""
Aggregates endpoint metadata getter.
Author: Maciej Cisowski
"""
from requests import Response
from common.helpers import get_api_key
from clients import client


def metadata(language: str = None) -> Response:
    headers = {}
    if language:
        headers.update({"Accept-Language": language})
    data = client.get(resource_path="aggregates/metadata", headers=headers)
    return data