from abc import ABC

from pybokio.client._base_client import BaseClient


class AccountingClient(BaseClient, ABC):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
