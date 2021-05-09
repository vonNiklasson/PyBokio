import abc
import enum
from abc import ABC

import requests
from requests import Response


class ConnectionMethod(enum.Enum):
    CREDENTIALS = enum.auto()
    COOKIES = enum.auto()


class BaseClient(ABC):
    @property
    @abc.abstractmethod
    def connection_method(self) -> ConnectionMethod:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def company_id(self) -> str:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def base_url(self) -> str:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def timeout(self) -> int:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def user_agent(self) -> str:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def session(self) -> requests.Session:
        raise NotImplementedError()

    @abc.abstractmethod
    def call_api(self, method: str, path: str, **kwargs) -> Response:
        raise NotImplementedError()
