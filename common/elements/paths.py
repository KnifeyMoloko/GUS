from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from logging import config as log_config
from typing import NamedTuple, Any

from common.helpers import get_config

logger = logging.getLogger(__name__)
log_config.dictConfig(get_config())


class RestMethod(NamedTuple):
    name: str

    def __str__(self):
        return self.name


class EndpointProperties(NamedTuple):
    parameters: list[dict[str, Any]]
    produces: list[str]
    responses: dict[str, dict[str, Any]]
    summary: str
    tags: list[str]


class RestMethods(NamedTuple):
    get: RestMethod = RestMethod("GET")


class ApiPath(ABC):
    def __init__(self, name: str, raw_path: str):
        self.__name = name
        self.__raw_path = raw_path

    def __repr__(self):
        return (
            f"{{ApiPath: {self.name}; raw_path: {self.raw_path}; "
            f"endpoint: {self.is_endpoint}}}"
        )

    def __eq__(self, other):
        if not isinstance(other, ApiPath):
            return NotImplemented
        return self.raw_path == other.raw_path

    @property
    def name(self) -> str:
        return self.__name

    @property
    def raw_path(self) -> str:
        return self.__raw_path

    @property
    @abstractmethod
    def is_endpoint(self) -> bool:
        ...


class GUSPath(ApiPath):
    def __init__(self, name: str, raw_path: str):
        super().__init__(name, raw_path)
        self.__sub_paths: list[GUSPath] = []
        self.__endpoints: list[GUSEndpoint] = []

    @property
    def is_endpoint(self) -> bool:
        return False

    @property
    def sub_paths(self) -> list[GUSPath]:
        return self.__sub_paths

    @property
    def endpoints(self) -> list[GUSEndpoint]:
        return self.__endpoints

    def register_subpath(self, subpath: GUSPath) -> bool:
        if subpath in self.sub_paths:
            logging.debug("Duplicate subpath found. Skipping the registration.")
            return False

        self.sub_paths.append(subpath)
        return True

    def register_endpoint(self, endpoint: GUSEndpoint) -> bool:
        if endpoint in self.endpoints:
            logging.debug("Duplicate endpoint found. Skipping the registration.")
            return False

        self.endpoints.append(endpoint)
        return True


class GUSEndpoint(ApiPath):
    def __init__(
        self,
        name: str,
        raw_path: str,
        method: RestMethod,
        properties: EndpointProperties,
    ):
        super().__init__(name, raw_path)
        self.__method = method
        self.__properties = properties

    @property
    def method(self):
        return self.__method

    @property
    def is_endpoint(self) -> bool:
        return True

    @property
    def parameters(self) -> list[dict[str, Any]]:
        return self.__properties.parameters

    @property
    def produces(self) -> list[str]:
        return self.__properties.produces

    @property
    def responses(self) -> dict[str, dict[str, Any]]:
        return self.__properties.responses

    @property
    def summary(self) -> str:
        return self.__properties.summary

    @property
    def tags(self) -> list[str]:
        return self.__properties.tags
