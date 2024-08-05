from enum import Enum


class TransactionResult(Enum):
    SUCCESS = "SUCCESS"
    PENDING = "PENDING"
    REDIRECTED = "REDIRECTED"
    ERROR = "ERROR"
    FAIL = "FAIL"


class TransactionType(Enum):
    MOTO = "MOTO"
    ECOM = "ECOM"
