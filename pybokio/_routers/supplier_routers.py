from typing import Dict

from requests import Response

from pybokio._routers.base_router import BaseRouter
from pybokio.exceptions import UnexpectedResponseError


class SupplierListSuppliersRouter(BaseRouter):
    _METHOD: str = "GET"
    _PATH: str = "<company_id>/Accounting/Suppliers/GetSuppliers"

    _JSON_SCHEMA: Dict = {
        "type": "object",
        "definitions": {
            "supplier": {
                "type": "object",
                "properties": {
                    "Id": {"type": "string"},
                },
            },
            "suppliers": {
                "type": "array",
                "items": {"$ref": "#/definitions/supplier"},
            },
        },
        "properties": {
            "Data": {"oneOf": [{"type": "null"}, {"$ref": "#/definitions/suppliers"}]},
            "Error": {"type": ["string", "integer"]},
            "Success": {"type": "boolean"},
            "ErrorMessage": {"type": ["string", "null"]},
        },
        "required": ["Data"],
    }

    def validate_response(self, response: Response):
        res = self._validate_json_response(response, self._JSON_SCHEMA)
