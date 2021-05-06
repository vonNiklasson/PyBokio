from typing import List

import requests
from requests import Response
from requests.sessions import RequestsCookieJar

from client.base_client import BaseClient
from utils.verification import is_json, is_valid_uuid4


class BokioClient(BaseClient):
    def __init__(
        self,
        company_id: str,
        username: str = None,
        password: str = None,
        base_url: str = BaseClient.DEFAULT_BASE_URL,
        timeout: int = 10,
    ):
        assert is_valid_uuid4(company_id), f'Parameter company_id "{company_id}" is not a valid UUID4 format.'

        self.__username: str = username
        self.__password: str = password
        self.__company_id: str = company_id
        self.__base_url: str = base_url.rstrip("/")
        self.__timeout: int = timeout

        self.__session = requests.session()

    @classmethod
    def from_cookiejar(
        cls,
        company_id: str,
        cookiejar: RequestsCookieJar,
        base_url: str = BaseClient.DEFAULT_BASE_URL,
        timeout: int = 10,
    ):
        client = cls(company_id=company_id, base_url=base_url, timeout=timeout)
        client.session.cookies.update(cookiejar)
        return client

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
    def session(self) -> requests.Session:
        return self.__session

    def login(self) -> List[str]:
        payload = {"userName": self.__username, "password": self.__password}
        response: Response = self._request("POST", "/Account/Login", json=payload)
        assert response.ok
        assert is_json(response)

        res = response.json()
        assert "Success" in res
        if res["Success"] is True:
            assert "Data" in res
            assert "CompanyIds" in res["Data"]
            company_ids = res["Data"]["CompanyIds"]
            assert type(company_ids) == list
            assert (
                self.company_id in company_ids
            ), f'company_id "{self.company_id}" not among allowed ids "{", ".join(company_ids)}"'
            return company_ids
        else:
            assert "Error" in res
            assert "ErrorMessage" in res
            exception_message = f"{res['Error']}: {res['ErrorMessage']}"
            raise Exception(exception_message)

    def logout(self) -> bool:
        pass

    def get_is_authenticated(self) -> bool:
        """
        Checks is the current session or credentials are authenticated.

        :return: True if the credentials or session are valid, otherwise False.
        """
        response: Response = self._request("GET", "/Account/IsAuthenticated")
        assert response.ok
        assert is_json(response)

        res = response.json()
        assert "Data" in res
        return res["Data"]
