from typing import Dict

from requests import Response

from pybokio._routers.base_router import BaseRouter
from pybokio.exceptions import UnexpectedResponseError


class AccountLoginRouter(BaseRouter):
    _METHOD: str = "POST"
    _PATH: str = "/Account/Login"

    _JSON_SCHEMA: Dict = {
        "type": "object",
        "definitions": {
            "login_data": {
                "type": "object",
                "properties": {
                    "CompanyIds": {"type": "array", "items": {"type": "string"}},
                    "UserName": {"type": "string"},
                },
            }
        },
        "properties": {
            "Data": {"oneOf": [{"type": "null"}, {"$ref": "#/definitions/login_data"}]},
            "Error": {"type": ["string", "null"]},
            "Success": {"type": "boolean"},
            "ErrorMessage": {"type": ["string", "null"]},
        },
        "required": ["Data", "Success", "Error", "ErrorMessage"],
    }

    def validate_response(self, response: Response):
        res = self._validate_json_response(response, self._JSON_SCHEMA)


class AccountIsAuthenticatedRouter(BaseRouter):
    _METHOD: str = "GET"
    _PATH: str = "/Account/IsAuthenticated"

    _JSON_SCHEMA: Dict = {
        "type": "object",
        "properties": {
            "Data": {"type": "boolean"},
            "Error": {"type": ["string", "null"]},
            "Success": {"type": "boolean"},
            "ErrorMessage": {"type": ["string", "null"]},
        },
        "required": ["Data"],
    }

    def validate_response(self, response: Response):
        res = self._validate_json_response(response, self._JSON_SCHEMA)


class AccountLogoutRouter(BaseRouter):
    _METHOD: str = "POST"
    _PATH: str = "/Account/LogOff"

    def validate_response(self, response: Response):
        if not response.ok:
            raise UnexpectedResponseError(f"Received status code {response.status_code} instead of 200")
