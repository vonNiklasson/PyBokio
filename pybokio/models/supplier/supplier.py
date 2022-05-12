from types import SimpleNamespace
from typing import Any, Optional


class Supplier(SimpleNamespace):
    class AddressObj(SimpleNamespace):
        Street1: Optional[str]
        Street2: Optional[str]
        City: Optional[str]
        PostalCode: Optional[str]
        Country: Optional[str]
        AddressString: Optional[str]

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

        if "Address" in kwargs:
            self.Address = Supplier.AddressObj(**kwargs["Address"])

    Id: str
    CompanyId: Optional[str]
    Name: Optional[str]
    OrgNumber: Optional[str]
    TaxRegistrationNumber: Optional[str]
    Address: AddressObj
    Email: Optional[str]
    Phone: Optional[str]
    ReferenceName: Optional[str]
    DefaultCurrencyCode: Optional[str]
    PaymentMethod: Optional[str]
    ExternalSystem: Optional[str]
