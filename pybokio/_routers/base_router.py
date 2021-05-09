import abc
from typing import Dict, List, Union

from jsonschema import exceptions as js_exceptions
from jsonschema import validate as validate_json
from requests import Response

from pybokio._utils.verification import is_response_json
from pybokio.exceptions._common import ExpectedJsonException, InvalidJsonSchemaException


class BaseRouter:
    _METHOD: str
    _PATH: str

    @staticmethod
    def _validate_json_response(response: Response, schema: Dict = None) -> Union[Dict, List, str]:
        """
        Validates that the response is JSON and adheres to the provided schema (optional).

        :param response: The response object to validate.
        :param schema: A schema to match the JSON against (optional).
        :return: Parsed JSON data from the response object.
        :raises UnexpectedResponseError: In case the response is malformed in any way.
        """
        if not is_response_json(response):
            raise ExpectedJsonException
        res = response.json()

        # If a schema is provided, make sure it matches
        if schema is not None:
            try:
                validate_json(res, schema)
            except js_exceptions.ValidationError:
                raise InvalidJsonSchemaException

        return res

    @abc.abstractmethod
    def validate_response(self, response: Response):
        ...

    @property
    def kwargs(self):
        return {"method": self.method, "path": self.path}

    @property
    def method(self) -> str:
        if not hasattr(self, "_METHOD"):
            raise NotImplementedError()
        return self._METHOD

    @property
    def path(self) -> str:
        if not hasattr(self, "_PATH"):
            raise NotImplementedError()
        return self._PATH
