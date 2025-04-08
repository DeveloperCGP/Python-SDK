from enum import Enum


class TransactionResult(Enum):
    SUCCESS = "SUCCESS"
    PENDING = "PENDING"
    REDIRECTED = "REDIRECTED"
    ERROR = "ERROR"
    FAIL = "FAIL"

    @staticmethod
    def get_by_status(value: str):
        for member in TransactionResult:
            if member.value == value:
                return member
        return None



class TransactionType(Enum):
    MOTO = "MOTO"
    ECOM = "ECOM"
