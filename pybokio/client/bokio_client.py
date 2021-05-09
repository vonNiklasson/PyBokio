import copy

import requests
from requests import Response
from requests.sessions import RequestsCookieJar

from pybokio import __version__
from pybokio.client._base_client import BaseClient, ConnectionMethod
from pybokio.client._subclients import AccountClient, AccountingClient
from pybokio.exceptions import AuthenticationError


class BokioClient(AccountClient, AccountingClient, BaseClient):

    DEFAULT_BASE_URL: str = "https://app.bokio.se"
    """
    The base URL of the bokio URL. Can be changed for testing purposes.
    """

    DEFAULT_USER_AGENT: str = f"PyBokio Client version {__version__} alpha (https://github.com/vonNiklasson/PyBokio)"
    """
    The user agent to be sent when making requests.
    """

    def __init__(
        self,
        company_id: str,
        username: str = None,
        password: str = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: int = 10,
        user_agent: str = DEFAULT_USER_AGENT,
    ):
        super().__init__(username, password)
        self.__connection_method: ConnectionMethod = ConnectionMethod.CREDENTIALS
        self.__username: str = username
        self.__password: str = password
        self.__company_id: str = company_id
        self.__base_url: str = base_url.rstrip("/")
        self.__timeout: int = timeout
        self.__user_agent: str = user_agent

        self.__session = requests.session()

    @classmethod
    def from_cookies(
        cls,
        company_id: str,
        cookies: RequestsCookieJar,
        base_url: str = DEFAULT_BASE_URL,
        timeout: int = 10,
        user_agent: str = DEFAULT_USER_AGENT,
    ):
        client = cls(company_id=company_id, base_url=base_url, timeout=timeout, user_agent=user_agent)
        client.__connection_method = ConnectionMethod.COOKIES
        client.session.cookies.update(cookies)
        return client

    @property
    def connection_method(self) -> ConnectionMethod:
        """
        The method used to establish a connection or authenticate to Bokio.
        """
        return self.__connection_method

    @property
    def company_id(self) -> str:
        """
        The company id currently being worked on with the client.
        """
        return self.__company_id

    @property
    def base_url(self) -> str:
        """
        The base url being used, for example https://www.bokio.se
        """
        return self.__base_url

    @property
    def timeout(self) -> int:
        """
        How long to wait during an API call before giving up.
        """
        return self.__timeout

    @property
    def user_agent(self) -> str:
        """
        The user agent sent to Bokio in the header.
        """
        return self.__user_agent

    @property
    def session(self) -> requests.Session:
        """
        The requests session that's being used to make calls.
        """
        return self.__session

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
        :param base_url: The base URL to append the path to.
        :return: A formatted URL possible to make queries to.
        """
        base_url = self.base_url if base_url is None else base_url
        url = f"{base_url}/{path.lstrip('/')}"
        url = url.replace("%company_id%", self.company_id)

        return url

    def call_api(self, method: str, path: str, **kwargs) -> Response:
        """
        Makes a request to Bokio.

        :param method: One of GET, POST, PUT, PATCH, DELETE, HEAD
        :param path: The path after bokio.se/... to call
        :param kwargs: Any extra parameters that will be sent to request(..., **kwargs)
        :return: The response of the request.
        """
        assert method.upper() in ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD"]

        # Add timeout to the kwargs if not passed
        if "timeout" not in kwargs:
            kwargs["timeout"] = self.timeout

        # Add the default user agent if not passed
        if "headers" not in kwargs:
            kwargs["headers"] = {"User-Agent": self.user_agent}

        url = self._prepare_url(path)
        response = self.session.request(method, url, **kwargs)
        return response

    def connect(self):
        """
        Attempts to connect to Bokio with the provided connection method.
        Will raise Exceptions if unable to do so.

        :raises AuthenticationError: If it wasn't possible to authenticate.
        """
        if self.connection_method == ConnectionMethod.CREDENTIALS:
            # account_login() will raise AuthenticationError if failing.
            self.account_login()
        elif self.connection_method == ConnectionMethod.COOKIES:
            is_authenticated = self.account_is_authenticated()
            if not is_authenticated:
                raise AuthenticationError("Provided cookies couldn't authenticate.")
