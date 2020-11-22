"""
Rest client implementation for GUS.
Author: Maciej Cisowski
"""
from Common.helpers import get_config
from Client.rest_client import RestClient
from logging import getLogger
from logging import config as log_config
from requests import Response


logger = getLogger(__name__)
log_config.dictConfig(get_config())


class GUSClient:
    def __init__(self,
                 ssl: bool,
                 host: str = None,
                 endpoint: str = None,
                 api_key: str = None):
        self.__client = RestClient(ssl=ssl,
                                   host="bdl.stat.gov.pl",
                                   endpoint="/api/v1/",
                                   api_key=api_key)

    @property
    def client(self) -> RestClient:
        return self.__client

    def get(self,
            resource_path: str,
            headers: dict) -> Response:
        logger.info(f"Fetching data from: \n\tpath:{resource_path}\n\theaders: {headers}")
        return self.client.get(resource_path=resource_path, additional_headers=headers)
