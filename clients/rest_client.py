"""
Generic REST client class.
Author: Maciej Cisowski
"""
import requests
import json
from logging import getLogger


logger = getLogger(__name__)


class RestClient(object):
    def __init__(self,
                 ssl: bool,
                 host: str = None,
                 endpoint: str = None,
                 api_key: str = None):
        """
        Create a Rest client instance for making http/s requests.
        :param ssl: should the client work in SSL mode or not
        :param api_key: optional for working with APIs needing keys
        """
        self.__url_prefix = "https://" if ssl else "http://"
        self.__host = host
        self.__endpoint = endpoint
        self.__api_key = api_key

    @property
    def api_key(self):
        return self.__api_key

    @property
    def url_prefix(self):
        return self.__url_prefix

    @property
    def host(self):
        return self.__host

    @property
    def endpoint(self):
        return self.__endpoint

    @endpoint.setter
    def endpoint(self, value):
        self.__endpoint = value

    def get(self, resource_path: str, additional_headers: dict = None) -> requests.Response:
        """
        Sends a GET method request to the host resource specified
        by the resource path. Returns a JSON type response and throws
        a ConnectionError in case of problems.
        :param resource_path: string with the path to the resource
        :param additional_headers: a dict of headers to add to the
        default ones
        :return: request response
        :rtype: json
        """
        # construct request headers
        headers = {"X-ClientId": self.api_key,
                   "Host": self.host,
                   "Content-Type": "application/json"}

        # add additional headers if needed
        if additional_headers:
            headers.update(additional_headers)

        logger.debug(f"Using headers: {headers}")

        # construct url string
        url = f"{self.__url_prefix}{self.__host}{self.__endpoint}{resource_path}"

        logger.info(f"Attempting a GET request for: {url}")
        return requests.get(url=url, params=None, headers=headers)
