import warnings
from typing import List

import requests
from requests import Response
from requests.sessions import RequestsCookieJar

from pybokio.client.base_client import BaseClient, ConnectionMethod
from pybokio.endpoints.account import AccountLoginEndpoint, AccountIsAuthenticatedEndpoint
from pybokio.exceptions import InvalidCredentialsError
from pybokio.utils.verification import is_response_json, is_valid_uuid4


class BokioClient(BaseClient):
    def __init__(
        self,
        company_id: str,
        username: str = None,
        password: str = None,
        base_url: str = BaseClient.DEFAULT_BASE_URL,
        timeout: int = 10,
        user_agent: str = BaseClient.DEFAULT_USER_AGENT,
    ):
        assert is_valid_uuid4(company_id), f'Parameter company_id "{company_id}" is not a valid UUID4 format.'

        self.__connection_method: ConnectionMethod = ConnectionMethod.CREDENTIALS
        self.__username: str = username
        self.__password: str = password
        self.__company_id: str = company_id
        self.__base_url: str = base_url.rstrip("/")
        self.__timeout: int = timeout
        self.__user_agent: str = user_agent

        self.__session = requests.session()

    @classmethod
    def from_cookiejar(
        cls,
        company_id: str,
        cookiejar: RequestsCookieJar,
        base_url: str = BaseClient.DEFAULT_BASE_URL,
        timeout: int = 10,
        user_agent: str = BaseClient.DEFAULT_USER_AGENT,
    ):
        client = cls(company_id=company_id, base_url=base_url, timeout=timeout, user_agent=user_agent)
        client.__connection_method = ConnectionMethod.SESSION
        client.session.cookies.update(cookiejar)
        return client

    @property
    def connection_method(self) -> ConnectionMethod:
        return self.__connection_method

    @property
    def company_id(self) -> str:
        return self.__company_id

    @property
    def base_url(self) -> str:
        return self.__base_url

    @property
    def timeout(self) -> int:
        return self.__timeout

    @property
    def user_agent(self) -> str:
        return self.__user_agent

    @property
    def session(self) -> requests.Session:
        return self.__session

    def connect(self):
        pass

    def account_login(self) -> List[str]:
        # Can only login when using credentials as initialisation method.
        if self.connection_method is not ConnectionMethod.CREDENTIALS:
            raise Exception("Cannot login when using cookiejar. Use connect() instead.")

        payload = {"userName": self.__username, "password": self.__password}
        endpoint = AccountLoginEndpoint()
        response: Response = self._request(**endpoint.kwargs)

        endpoint.validate_response(response)
        res = response.json()

        if res["Success"] is True:
            company_ids = res["Data"]["CompanyIds"]
            if self.company_id not in company_ids:
                warnings.warn(f'company_id "{self.company_id}" not among allowed ids "{", ".join(company_ids)}"')
            return company_ids
        else:
            error_code = res["Error"]
            error_message = res["ErrorMessage"]
            exception_message = f"{error_code}: {error_message}"

            if error_code == "UserNotFound" or error_code == "InvalidPassword":
                raise InvalidCredentialsError(exception_message)
            else:
                raise Exception(exception_message)

    def account_logout(self) -> bool:
        pass

    def account_is_authenticated(self) -> bool:
        """
        Checks is the current session or credentials are authenticated.

        :return: True if the credentials or session are valid, otherwise False.
        """
        endpoint = AccountIsAuthenticatedEndpoint()
        response: Response = self._request(**endpoint.kwargs)
        endpoint.validate_response(response)
        res = response.json()
        return res["Data"]
