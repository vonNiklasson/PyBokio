from typing import Dict

from requests import Response

from pybokio._routers.base_router import BaseRouter
from pybokio.exceptions import UnexpectedResponseError


class FileUploadReceiptPdfRouter(BaseRouter):
    _METHOD: str = "POST"
    _PATH: str = "<company_id>/Accounting/Receipt/UploadPdf"

    _JSON_SCHEMA: Dict = {
        "type": "object",
        "properties": {
            "Id": {"type": ["string"]},
        },
        "required": ["Id"],
    }

    def validate_response(self, response: Response):
        res = self._validate_json_response(response, self._JSON_SCHEMA)


class FileDeleteReceiptsRouter(BaseRouter):
    _METHOD: str = "POST"
    _PATH: str = "<company_id>/Accounting/Receipt/BatchDelete"

    _JSON_SCHEMA: Dict = {
        "type": "object",
        "properties": {
            "Data": {"type": "boolean"},
            "Error": {"type": ["string", "integer"]},
            "Success": {"type": "boolean"},
            "ErrorMessage": {"type": ["string", "null"]},
        },
        "required": ["Success"],
    }

    def validate_response(self, response: Response):
        res = self._validate_json_response(response, self._JSON_SCHEMA)


class FileListReceiptsRouter(BaseRouter):
    _METHOD: str = "GET"
    _PATH: str = (
        "<company_id>/Accounting/Receipt/ListAllReceiptsForUploadsScene?includeBookkeptItems=<include_bookkept>"
    )

    def __init__(self, include_bookkept: bool):
        self.include_bookkept = include_bookkept

    def prepare_path(self):
        path = super().prepare_path()
        return path.replace("<include_bookkept>", str(self.include_bookkept).lower())

    _JSON_SCHEMA: Dict = {
        "type": "object",
        "definitions": {
            "receipt": {
                "type": "object",
                "properties": {
                    "Id": {"type": "string"},
                    "Category": {"type": "string"},
                    "UploadedDate": {"type": "string"},
                },
            },
            "receipts": {
                "type": "object",
                "properties": {"Receipts": {"type": "array", "items": {"$ref": "#/definitions/receipt"}}},
            },
        },
        "properties": {
            "Data": {"oneOf": [{"type": "null"}, {"$ref": "#/definitions/receipts"}]},
            "Error": {"type": ["string", "integer"]},
            "Success": {"type": "boolean"},
            "ErrorMessage": {"type": ["string", "null"]},
        },
        "required": ["Data"],
    }

    def validate_response(self, response: Response):
        res = self._validate_json_response(response, self._JSON_SCHEMA)
