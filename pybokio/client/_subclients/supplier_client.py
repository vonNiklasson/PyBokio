from typing import List

from requests import Response

from pybokio._routers.supplier_routers import SupplierListSuppliersRouter
from pybokio.client._subclients._base_sub_client import BaseSubClient
from pybokio.models.supplier import Supplier


class SupplierClient(BaseSubClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def list_suppliers(self) -> List[Supplier]:
        endpoint = SupplierListSuppliersRouter()
        response: Response = self.client.call_api(**endpoint.kwargs)

        endpoint.validate_response(response)
        res = response.json()

        return [Supplier(**supplier) for supplier in res["Data"]]
