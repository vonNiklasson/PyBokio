from types import SimpleNamespace
from typing import Any, List, Optional


class ListedReceipt(SimpleNamespace):
    class ExtraPage(SimpleNamespace):
        Id: str
        ReceiptId: str
        PageNumber: int
        IsPdf: bool

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

        if "ExtraPages" in kwargs:
            self.ExtraPages = [self.ExtraPage(**page) for page in kwargs["ExtraPages"]]

    Description: Optional[str]
    PredictedTotalSum: Optional[float]
    PredictedPaymentDate: Optional[str]
    PredictedDate: Optional[str]
    Category: str
    VerificationId: Optional[str]
    PaymentDate: Optional[str]
    TotalSum: Optional[float]
    AutoVerificationRowId: Optional[str]
    IsPdf: bool
    Attested: bool
    IsAutoVerificationRowPending: bool
    IsNonSignedOrScheduledPayment: bool
    PaymentStatus: Optional[Any]
    ManualPaymentId: Optional[str]
    Id: str
    UploadedDate: Optional[str]
    Date: Optional[str]
    Version: int
    UploadedByUser: str
    ExtraPages: List[ExtraPage]
