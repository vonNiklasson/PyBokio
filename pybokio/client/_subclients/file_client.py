from typing import List, Union

from requests import Response

from pybokio._routers.file_routers import (
    FileDeleteReceiptsRouter,
    FileListReceiptsRouter,
    FileUploadReceiptPdfRouter,
)
from pybokio.client._subclients._base_sub_client import BaseSubClient
from pybokio.options import FileUploadReceiptCategories


class FileClient(BaseSubClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def upload_receipt_pdf(
        self, file_path, category: FileUploadReceiptCategories = FileUploadReceiptCategories.UNKNOWN
    ) -> str:
        data = {"selectedType": category.value, "startRecepiptPredictionsNow": True}
        files = {"file": open(file_path, "rb")}
        endpoint = FileUploadReceiptPdfRouter()
        response: Response = self.client.call_api(**endpoint.kwargs, data=data, files=files)

        endpoint.validate_response(response)
        res = response.json()

        return res["Id"]

    def list_receipts(self) -> List[str]:
        endpoint = FileListReceiptsRouter()
        response: Response = self.client.call_api(**endpoint.kwargs)

        endpoint.validate_response(response)
        res = response.json()

        return [receipt["Id"] for receipt in res["Data"]["Receipts"]]

    def delete_receipts(self, receipts: Union[str, List[str]]) -> None:
        if type(receipts) is str:
            receipts = [receipts]

        payload = {"ReceiptIds": receipts}

        endpoint = FileDeleteReceiptsRouter()
        response: Response = self.client.call_api(**endpoint.kwargs, json=payload)

        endpoint.validate_response(response)
        res = response.json()
