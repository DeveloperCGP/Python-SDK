from typing import Tuple

from sdk.enums.payment_solutions import PaymentSolutions
from sdk.exceptions.field_exception import InvalidFieldException
from sdk.models.credentials import Credentials
from sdk.utils.general_utils import GeneralUtils


class H2HVoid:
    __merchantId: str = None
    __paymentSolution: PaymentSolutions = None
    __transactionId: str = None
    __merchantTransactionId: str = None
    __description: str = None

    def get_merchant_id(self):
        return self.__merchantId

    def get_merchant_transaction_id(self):
        return self.__merchantTransactionId

    def set_merchant_transaction_id(self, new_merchant_transaction_id: str):
        if new_merchant_transaction_id is None or not new_merchant_transaction_id or len(
                new_merchant_transaction_id) > 45:
            raise InvalidFieldException(
                "merchantTransactionId: Invalid Size, size must be (0 < merchantTransactionId <= 45)")
        self.__merchantTransactionId = new_merchant_transaction_id

    def get_payment_solution(self):
        return self.__paymentSolution

    def set_payment_solution(self, new_payment_solution: PaymentSolutions):
        self.__paymentSolution = new_payment_solution

    def get_transaction_id(self):
        return self.__transactionId

    def set_transaction_id(self, new_transaction_id: str):
        if new_transaction_id is None or not new_transaction_id.isdigit() or len(new_transaction_id) > 100:
            raise InvalidFieldException("transactionId: Must be numbers only with size (transactionId <= 100)")
        self.__transactionId = new_transaction_id

    def get_description(self):
        return self.__description

    def set_description(self, new_description: str):
        if len(new_description) > 1000:
            raise InvalidFieldException("description: Invalid Size, size must be (description <= 1000)")
        self.__description = new_description

    def set_credentials(self, new_credentials: Credentials):
        if new_credentials is None:
            raise InvalidFieldException("credentials")
        self.__merchantId = new_credentials.get_merchant_id()

    def is_missing_field(self) -> Tuple[bool, any]:
        mandatory_fields = {
            "merchantId": self.__merchantId,
            "paymentSolution": self.__paymentSolution,
            "transactionId": self.__transactionId,
            "merchantTransactionId": self.__merchantTransactionId
        }

        return GeneralUtils.contains_null(mandatory_fields)

    def check_credentials(self, credentials: Credentials) -> Tuple[bool, any]:
        if credentials.get_api_version() < 0:
            return True, "apiVersion"

        mandatory_fields = {
            "merchantId": credentials.get_merchant_id(),
            "merchantPass": credentials.get_merchant_pass(),
            "environment": credentials.get_environment().value
        }

        return GeneralUtils.contains_null(mandatory_fields)
