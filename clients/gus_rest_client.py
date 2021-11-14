"""
Rest client implementation for GUS.
Author: Maciej Cisowski
"""
from logging import config as log_config
from logging import getLogger

from requests import Response  # type: ignore

from clients.rest_client import RestClient
from common.helpers import get_config

logger = getLogger(__name__)
log_config.dictConfig(get_config())


class GUSClient:
    def __init__(self, ssl: bool, api_key: str = None):
        self.__client = RestClient(
            ssl=ssl, host="bdl.stat.gov.pl", endpoint="/api/v1/", api_key=api_key
        )

    @property
    def client(self) -> RestClient:
        return self.__client

    def get(self, resource_path: str, headers: dict) -> Response:
        logger.info(
            "Fetching data from: \n\tpath:%s\n\theaders: %s", resource_path, headers
        )
        return self.client.get(resource_path=resource_path, additional_headers=headers)
