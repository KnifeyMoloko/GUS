"""
Rest client implementation for GUS.
Author: Maciej Cisowski
"""
from Rest import RestClient
from logging import getLogger


logger = getLogger(__name__)


class PLStatClient:
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


