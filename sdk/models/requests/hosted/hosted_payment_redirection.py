from typing import List, Optional, Tuple

from sdk.enums.country_code import CountryCodeAlpha2
from sdk.enums.currency import Currency
from sdk.enums.language import Language
from sdk.enums.operation_types import OperationTypes
from sdk.enums.payment_solutions import PaymentSolutions
from sdk.enums.transaction import TransactionType
from sdk.exceptions.field_exception import InvalidFieldException
from sdk.models.credentials import Credentials
from sdk.utils.general_utils import GeneralUtils


class HostedPaymentRedirection:
    __merchantId: Optional[str] = None
    __productId: Optional[str] = None
    __paymentSolution: Optional[PaymentSolutions] = None
    __operationType: OperationTypes = None
    __merchantTransactionId: str = None
    __amount: Optional[str] = None
    __currency: Optional[Currency] = None
    __country: Optional[CountryCodeAlpha2] = None
    __customerId: Optional[str] = None
    __statusURL: Optional[str] = None
    __successURL: Optional[str] = None
    __errorURL: Optional[str] = None
    __cancelURL: Optional[str] = None
    __awaitingURL: Optional[str] = None
    __language: Optional[Language] = None
    __referenceId: Optional[str] = None
    __printReceipt: bool = False
    __type: TransactionType = None
    __autoCapture: bool = True
    __description: Optional[str] = None
    __forceTokenRequest: bool = False
    __showRememberMe: bool = False
    __merchantParams: Optional[List[Tuple[str, str]]] = None

    def __init__(self):
        self.__merchantTransactionId = GeneralUtils.generate_random_number()
        self.__operationType = OperationTypes.DEBIT
        self.__type = TransactionType.ECOM

    def get_currency(self) -> Optional[Currency]:
        return self.__currency

    def set_currency(self, currency: Currency):
        self.__currency = currency

    def get_amount(self) -> Optional[str]:
        return self.__amount

    def set_amount(self, amount):
        parsed_amount = GeneralUtils.parse_amount(amount)
        if parsed_amount is None:
            raise InvalidFieldException(
                "amount: Should Follow Format #.#### And Be Between 0 And 1000000"
            )
        self.__amount = parsed_amount

    def get_country(self) -> Optional[CountryCodeAlpha2]:
        return self.__country

    def set_country(self, country: CountryCodeAlpha2):
        self.__country = country

    def get_customer_id(self) -> Optional[str]:
        return self.__customerId

    def set_customer_id(self, customer_id: str):
        if len(customer_id) > 80:
            raise InvalidFieldException(
                "customerId: Invalid Size, size must be (0 < customerId <= 80)"
            )
        self.__customerId = customer_id

    def get_merchant_id(self) -> Optional[str]:
        return self.__merchantId

    def get_merchant_transaction_id(self) -> str:
        return self.__merchantTransactionId

    def set_merchant_transaction_id(self, merchant_transaction_id: str):
        if not merchant_transaction_id or len(merchant_transaction_id) > 45:
            raise InvalidFieldException(
                "merchantTransactionId: Invalid Size, size must be (0 < merchantTransactionId <= 45)"
            )
        self.__merchantTransactionId = merchant_transaction_id

    def get_payment_solution(self) -> Optional[PaymentSolutions]:
        return self.__paymentSolution

    def set_payment_solution(self, payment_solution: PaymentSolutions):
        self.__paymentSolution = payment_solution

    def get_status_url(self) -> Optional[str]:
        return self.__statusURL

    def set_status_url(self, status_url: str):
        if not GeneralUtils.is_valid_url(status_url):
            raise InvalidFieldException("statusURL")
        self.__statusURL = status_url

    def get_error_url(self) -> Optional[str]:
        return self.__errorURL

    def set_error_url(self, error_url: str):
        if not GeneralUtils.is_valid_url(error_url):
            raise InvalidFieldException("errorURL")
        self.__errorURL = error_url

    def get_success_url(self) -> Optional[str]:
        return self.__successURL

    def set_success_url(self, success_url: str):
        if not GeneralUtils.is_valid_url(success_url):
            raise InvalidFieldException("successURL")
        self.__successURL = success_url

    def get_cancel_url(self) -> Optional[str]:
        return self.__cancelURL

    def set_cancel_url(self, cancel_url: str):
        if not GeneralUtils.is_valid_url(cancel_url):
            raise InvalidFieldException("cancelURL")
        self.__cancelURL = cancel_url

    def get_awaiting_url(self) -> Optional[str]:
        return self.__awaitingURL

    def set_awaiting_url(self, awaiting_url: str):
        if not GeneralUtils.is_valid_url(awaiting_url):
            raise InvalidFieldException("awaitingURL")
        self.__awaitingURL = awaiting_url

    def get_product_id(self) -> Optional[str]:
        return self.__productId

    def get_operation_type(self) -> OperationTypes:
        return self.__operationType

    def set_operation_type(self, operation_type: OperationTypes):
        self.__operationType = operation_type

    def is_force_token_request(self) -> bool:
        return self.__forceTokenRequest

    def set_force_token_request(self, force_token_request: bool):
        self.__forceTokenRequest = force_token_request

    def is_show_remember_me(self) -> bool:
        return self.__showRememberMe

    def set_show_remember_me(self, show_remember_me: bool):
        self.__showRememberMe = show_remember_me

    def get_language(self) -> Optional[Language]:
        return self.__language

    def set_language(self, language: Language):
        self.__language = language

    def get_reference_id(self) -> Optional[str]:
        return self.__referenceId

    def set_reference_id(self, reference_id: str):
        if len(reference_id) != 12:
            raise InvalidFieldException("referenceId: Invalid Size, size must be (referenceId = 12)")
        self.__referenceId = reference_id

    def is_print_receipt(self) -> bool:
        return self.__printReceipt

    def set_print_receipt(self, print_receipt: bool):
        self.__printReceipt = print_receipt

    def get_type(self) -> TransactionType:
        return self.__type

    def set_type(self, transaction_type: TransactionType):
        self.__type = transaction_type

    def is_auto_capture(self) -> bool:
        return self.__autoCapture

    def set_auto_capture(self, auto_capture: bool):
        self.__autoCapture = auto_capture

    def get_description(self) -> Optional[str]:
        return self.__description

    def set_description(self, description: str):
        if len(description) > 1000:
            raise InvalidFieldException("description: Invalid Size, size must be (description <= 1000)")
        self.__description = description

    def set_merchant_params(self, merchant_params: List[Tuple[str, str]]):
        if self.__merchantParams is None:
            self.__merchantParams = merchant_params
        else:
            self.__merchantParams.extend(merchant_params)
        if len(GeneralUtils.merchant_params_query(self.__merchantParams)) > 500:
            raise InvalidFieldException("merchantParams: Invalid Size, Size Must Be merchantParams <= 100")

    def get_merchant_param(self) -> Optional[List[Tuple[str, str]]]:
        return self.__merchantParams

    def set_merchant_param(self, key: str, value: str):
        if self.__merchantParams is None:
            self.__merchantParams = []
        self.__merchantParams.append((key, value))
        if len(GeneralUtils.merchant_params_query(self.__merchantParams)) > 500:
            raise InvalidFieldException("merchantParams: Invalid Size, Size Must Be merchantParams <= 100")

    def set_credentials(self, credentials: Credentials):
        self.__merchantId = credentials.get_merchant_id()
        self.__productId = credentials.get_product_id()

    def is_missing_field(self) -> Tuple[bool, str]:
        mandatory_fields = {
            "currency": self.__currency,
            "amount": self.__amount,
            "country": self.__country,
            "customerId": self.__customerId,
            "merchantId": self.__merchantId,
            "merchantTransactionId": self.__merchantTransactionId,
            "paymentSolution": self.__paymentSolution,
            "statusURL": self.__statusURL,
            "successURL": self.__successURL,
            "errorURL": self.__errorURL,
            "cancelURL": self.__cancelURL,
            "awaitingURL": self.__awaitingURL,
            "productId": self.__productId,
            "operationType": self.__operationType
        }

        return GeneralUtils.contains_null(mandatory_fields)

    @staticmethod
    def check_credentials(credentials: Credentials) -> Tuple[bool, Optional[str]]:
        if credentials.get_api_version() < 0:
            return True, "apiVersion"

        mandatory_fields = {
            "merchantId": credentials.get_merchant_id(),
            "productId": credentials.get_product_id(),
            "merchantPass": credentials.get_merchant_pass(),
            "environment": credentials.get_environment().value
        }

        return GeneralUtils.contains_null(mandatory_fields)
