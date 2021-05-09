import abc
import copy
import enum

import requests
from requests import Response
from requests.cookies import RequestsCookieJar

from pybokio import __version__


class ConnectionMethod(enum.Enum):
    CREDENTIALS = enum.auto()
    COOKIES = enum.auto()


class BaseClient(metaclass=abc.ABCMeta):

    DEFAULT_BASE_URL: str = "https://app.bokio.se"
    """
    The base URL of the bokio URL. Can be changed for testing purposes.
    """

    DEFAULT_USER_AGENT: str = f"PyBokio Client version {__version__} alpha (https://github.com/vonNiklasson/PyBokio)"
    """
    The user agent to be used when making requests.
    """

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

    def get_cookies(self) -> RequestsCookieJar:
        """
        Returns a copy of the cookies associated with the current session.

        :return: The cookies from the current session.
        """
        return copy.deepcopy(self.session.cookies)

    def _prepare_url(self, path: str, base_url: str = None) -> str:
        """
        Prepares the URL by adding the base url and adding company id where applicable.

        :param path: The path after the base url to do a request to.
        :param base_url:
        :return:
        """
        base_url = self.base_url if base_url is None else base_url
        url = f"{base_url}/{path.lstrip('/')}"
        url = url.replace("%company_id%", self.company_id)

        return url

    def _request(self, method: str, path: str, **kwargs) -> Response:
        assert method.upper() in ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD"]

        # Add timeout to the kwargs if not passed
        if "timeout" not in kwargs:
            kwargs["timeout"] = self.timeout

        # Add the default user agent if not passed
        if "user_agent" not in kwargs:
            kwargs["headers"] = {"User-Agent": self.user_agent}

        url = self._prepare_url(path)
        response = self.session.request(method, url, **kwargs)
        return response
