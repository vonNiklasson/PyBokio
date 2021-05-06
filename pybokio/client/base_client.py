import abc
import copy

import requests
from requests import Response
from requests.cookies import RequestsCookieJar


class BaseClient(metaclass=abc.ABCMeta):

    DEFAULT_BASE_URL: str = "https://app.bokio.se"
    """
    The base URL of the bokio URL. Can be changed for testing purposes.
    """

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
    def session(self) -> requests.Session:
        raise NotImplementedError()

    def get_cookiejar(self) -> RequestsCookieJar:
        """
        Returns a copy of the cookiejar associated with the current session.

        :return: The cookiejar from the current session.
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

        # Add timeout to the kwargs if not already present
        if "timeout" not in kwargs:
            kwargs["timeout"] = self.timeout

        url = self._prepare_url(path)
        response = self.session.request(method, url, **kwargs)
        return response
