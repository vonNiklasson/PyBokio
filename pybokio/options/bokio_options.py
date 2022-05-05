import enum


class AccountingUploadReceiptCategories(enum.Enum):
    EXPENSES = "expense"
    INCOME = "income"
    OTHER = "other"
    SUPPLIER = "supplier"
    UNKNOWN = None
