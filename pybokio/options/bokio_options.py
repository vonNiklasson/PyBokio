import enum


class FileUploadReceiptCategories(enum.Enum):
    EXPENSES = "expense"
    INCOME = "income"
    OTHER = "other"
    SUPPLIER = "supplier"
    UNKNOWN = None
