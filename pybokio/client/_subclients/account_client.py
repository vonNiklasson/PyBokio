import warnings
from typing import List

from requests import Response

from pybokio._routers.account_routers import AccountIsAuthenticatedRouter, AccountLoginRouter, AccountLogoutRouter
from pybokio.client._subclients._base_sub_client import BaseSubClient
from pybokio.exceptions import AuthenticationError
from pybokio.options import ConnectionMethod


class AccountClient(BaseSubClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__username = kwargs.get("username", None)
        self.__password = kwargs.get("password", None)

    def login(self) -> List[str]:
        """
        Logs in to the account and store the session for subsequent api calls.
        Can only be called if using credentials to authenticate, otherwise connect() should be used.

        :return: A list of associated company ids to the user.
        :raises ConnectionError: If trying to login when using cookies to authenticate.
        :raises AuthenticationError: If the credentials are invalid.
        """
        # Can only login when using credentials as initialisation method.
        if self.client.connection_method is not ConnectionMethod.CREDENTIALS:
            raise ConnectionError("Cannot login when using cookies. Use BokioClient.connect() instead.")

        payload = {"userName": self.__username, "password": self.__password}
        endpoint = AccountLoginRouter()
        response: Response = self.client.call_api(**endpoint.kwargs, json=payload)

        endpoint.validate_response(response)
        res = response.json()

        if res["Success"] is True:
            company_ids = res["Data"]["CompanyIds"]
            if self.client.company_id not in company_ids:
                warnings.warn(f'company_id "{self.client.company_id}" not among allowed ids "{", ".join(company_ids)}"')
            return company_ids
        else:
            error_code = res["Error"]
            error_message = res["ErrorMessage"]
            exception_message = f"{error_code}: {error_message}"

            if error_code == "UserNotFound" or error_code == "InvalidPassword":
                raise AuthenticationError(exception_message)
            else:
                raise Exception(exception_message)

    def logout(self) -> None:
        """
        Logs out from the current session. Will not return anything.
        """
        endpoint = AccountLogoutRouter()
        response: Response = self.client.call_api(**endpoint.kwargs)

    def is_authenticated(self) -> bool:
        """
        Checks is the current session or credentials are authenticated.

        :return: True if the credentials or session are valid, otherwise False.
        """
        endpoint = AccountIsAuthenticatedRouter()
        response: Response = self.client.call_api(**endpoint.kwargs)
        endpoint.validate_response(response)
        res = response.json()
        return res["Data"]
