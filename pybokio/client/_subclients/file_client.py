from typing import List, Union

from requests import Response

from pybokio._routers.file_routers import FileDeleteReceiptsRouter, FileListReceiptsRouter, FileUploadReceiptPdfRouter
from pybokio.client._subclients._base_sub_client import BaseSubClient
from pybokio.models.file import Receipt
from pybokio.options import FileUploadReceiptCategories


class FileClient(BaseSubClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def upload_receipt_pdf(
        self, file_path, category: FileUploadReceiptCategories = FileUploadReceiptCategories.UNKNOWN
    ) -> Receipt:
        data = {"selectedType": category.value, "startReceiptPredictionsNow": True}
        files = {"file": open(file_path, "rb")}
        endpoint = FileUploadReceiptPdfRouter()
        response: Response = self.client.call_api(**endpoint.kwargs, data=data, files=files)

        endpoint.validate_response(response)
        res = response.json()

        return Receipt(**res)

    def list_receipts(self, include_bookkept: bool = False) -> List[Receipt]:
        endpoint = FileListReceiptsRouter(include_bookkept=include_bookkept)
        response: Response = self.client.call_api(**endpoint.kwargs)

        endpoint.validate_response(response)
        res = response.json()

        return [Receipt(**receipt) for receipt in res["Data"]["Receipts"]]

    def delete_receipts(self, receipts: List[Union[str, Receipt]]) -> None:
        receipt_ids = [receipt.Id if isinstance(receipt, Receipt) else receipt for receipt in receipts]

        payload = {"ReceiptIds": receipt_ids}

        endpoint = FileDeleteReceiptsRouter()
        response: Response = self.client.call_api(**endpoint.kwargs, json=payload)

        endpoint.validate_response(response)
        res = response.json()

    def delete_receipt(self, receipt: Union[str, Receipt]) -> None:
        return self.delete_receipts([receipt])
