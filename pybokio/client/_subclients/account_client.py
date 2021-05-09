import warnings
from abc import ABC
from typing import List

from requests import Response

from pybokio._routers.account_routers import AccountIsAuthenticatedRouter, AccountLoginRouter, AccountLogoutRouter
from pybokio.client._base_client import BaseClient, ConnectionMethod
from pybokio.exceptions import AuthenticationError


class AccountClient(BaseClient, ABC):
    def __init__(self, username: str, password: str):
        self.__username = username
        self.__password = password

    def account_login(self) -> List[str]:
        # Can only login when using credentials as initialisation method.
        if self.connection_method is not ConnectionMethod.CREDENTIALS:
            raise Exception("Cannot login when using cookies. Use connect() instead.")

        payload = {"userName": self.__username, "password": self.__password}
        endpoint = AccountLoginRouter()
        response: Response = self.call_api(**endpoint.kwargs, json=payload)

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
                raise AuthenticationError(exception_message)
            else:
                raise Exception(exception_message)

    def account_logout(self):
        """
        Logs out from the current session. Will not return anything.
        """
        endpoint = AccountLogoutRouter()
        response: Response = self.call_api(**endpoint.kwargs)

    def account_is_authenticated(self) -> bool:
        """
        Checks is the current session or credentials are authenticated.

        :return: True if the credentials or session are valid, otherwise False.
        """
        endpoint = AccountIsAuthenticatedRouter()
        response: Response = self.call_api(**endpoint.kwargs)
        endpoint.validate_response(response)
        res = response.json()
        return res["Data"]
