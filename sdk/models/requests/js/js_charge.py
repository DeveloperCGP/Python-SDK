from typing import List, Tuple

from sdk.enums.country_code import CountryCodeAlpha2
from sdk.enums.currency import Currency
from sdk.enums.language import Language
from sdk.enums.operation_types import OperationTypes
from sdk.enums.payment_solutions import PaymentSolutions
from sdk.enums.transaction import TransactionType
from sdk.exceptions.field_exception import InvalidFieldException
from sdk.models.credentials import Credentials
from sdk.utils.general_utils import GeneralUtils


class JSCharge:
    __prepayToken: str = None
    __merchantId: str = None
    __apiVersion: int = -1
    __paymentSolution: PaymentSolutions = None
    __operationType: OperationTypes = None
    __merchantTransactionId: str = None
    __amount: str = None
    __currency: Currency = None
    __country: CountryCodeAlpha2 = None
    __customerId: str = None
    __statusURL: str = None
    __successURL: str = None
    __errorURL: str = None
    __cancelURL: str = None
    __awaitingURL: str = None
    __productId: str = None
    __language: Language = None
    __referenceId: str = None
    __merchantParams: List[Tuple[str, str]] = None
    __forceTokenRequest: bool = False
    __printReceipt: bool = False
    __type: TransactionType = None
    __autoCapture: bool = True
    __description: str = None

    def __init__(self):
        self.__apiVersion = -1
        self.__operationType = OperationTypes.DEBIT
        self.__merchantTransactionId = GeneralUtils.generate_random_number()
        self.__type = TransactionType.ECOM

    def get_currency(self) -> Currency:
        return self.__currency

    def set_currency(self, currency: Currency) -> None:
        self.__currency = currency

    def get_merchant_id(self) -> str:
        return self.__merchantId

    def get_product_id(self) -> str:
        return self.__productId

    def get_country(self) -> CountryCodeAlpha2:
        return self.__country

    def set_country(self, country: CountryCodeAlpha2) -> None:
        self.__country = country

    def get_customer_id(self) -> str:
        return self.__customerId

    def set_customer_id(self, customer_id: str) -> None:
        if customer_id is None or len(customer_id) == 0 or len(customer_id) > 80:
            raise InvalidFieldException("customer_id: Invalid Size, size must be (0 < customer_id <= 80)")
        self.__customerId = customer_id

    def get_amount(self) -> str:
        return self.__amount

    def set_amount(self, amount) -> None:
        parsed_amount = GeneralUtils.parse_amount(amount)
        if parsed_amount is None:
            raise InvalidFieldException("amount: Should Follow Format #.#### And Be Between 0 And 1000000")
        self.__amount = parsed_amount

    def get_merchant_transaction_id(self) -> str:
        return self.__merchantTransactionId

    def set_merchant_transaction_id(self, merchant_transaction_id: str) -> None:
        if not merchant_transaction_id or len(merchant_transaction_id) > 45:
            raise InvalidFieldException(
                "merchant_transaction_id: Invalid Size, size must be (0 < merchant_transaction_id <= 45)")
        self.__merchantTransactionId = merchant_transaction_id

    def get_operation_type(self) -> OperationTypes:
        return self.__operationType

    def set_operation_type(self, operation_type: OperationTypes) -> None:
        self.__operationType = operation_type

    def get_prepay_token(self) -> str:
        return self.__prepayToken

    def set_prepay_token(self, prepay_token: str) -> None:
        self.__prepayToken = prepay_token

    def get_status_url(self) -> str:
        return self.__statusURL

    def set_status_url(self, status_url: str) -> None:
        if not GeneralUtils.is_valid_url(status_url):
            raise InvalidFieldException("status_url")
        self.__statusURL = status_url

    def get_success_url(self) -> str:
        return self.__successURL

    def set_success_url(self, success_url: str) -> None:
        if not GeneralUtils.is_valid_url(success_url):
            raise InvalidFieldException("statusURL: Must be a valid url")
        self.__successURL = success_url

    def get_error_url(self) -> str:
        return self.__errorURL

    def set_error_url(self, error_url: str) -> None:
        if not GeneralUtils.is_valid_url(error_url):
            raise InvalidFieldException("error_url")
        self.__errorURL = error_url

    def get_cancel_url(self) -> str:
        return self.__cancelURL

    def set_cancel_url(self, cancel_url: str) -> None:
        if not GeneralUtils.is_valid_url(cancel_url):
            raise InvalidFieldException("cancel_url")
        self.__cancelURL = cancel_url

    def get_awaiting_url(self) -> str:
        return self.__awaitingURL

    def set_awaiting_url(self, awaiting_url: str) -> None:
        if not GeneralUtils.is_valid_url(awaiting_url):
            raise InvalidFieldException("awaiting_url")
        self.__awaitingURL = awaiting_url

    def get_payment_solution(self) -> PaymentSolutions:
        return self.__paymentSolution

    def set_payment_solution(self, payment_solution: PaymentSolutions) -> None:
        self.__paymentSolution = payment_solution

    def get_api_version(self) -> int:
        return self.__apiVersion

    def is_force_token_request(self) -> bool:
        return self.__forceTokenRequest

    def set_force_token_request(self, force_token_request: bool) -> None:
        self.__forceTokenRequest = force_token_request

    def get_language(self) -> Language:
        return self.__language

    def set_language(self, language: Language) -> None:
        self.__language = language

    def get_reference_id(self) -> str:
        return self.__referenceId

    def set_reference_id(self, reference_id: str) -> None:
        if len(reference_id) != 12:
            raise InvalidFieldException("reference_id: Invalid Size, size must be (reference_id = 12)")
        self.__referenceId = reference_id

    def is_print_receipt(self) -> bool:
        return self.__printReceipt

    def set_print_receipt(self, print_receipt: bool) -> None:
        self.__printReceipt = print_receipt

    def get_type(self) -> TransactionType:
        return self.__type

    def set_type(self, transaction_type: TransactionType) -> None:
        self.__type = transaction_type

    def is_auto_capture(self) -> bool:
        return self.__autoCapture

    def set_auto_capture(self, auto_capture: bool) -> None:
        self.__autoCapture = auto_capture

    def get_description(self) -> str:
        return self.__description

    def set_description(self, description: str) -> None:
        if len(description) > 1000:
            raise InvalidFieldException("description: Invalid Size, size must be (description <= 1000)")
        self.__description = description

    def set_merchant_params(self, merchant_params: List[Tuple[str, str]]) -> None:
        if self.__merchantParams is None:
            self.__merchantParams = merchant_params
        else:
            self.__merchantParams.extend(merchant_params)
        if len(GeneralUtils.merchant_params_query(self.__merchantParams)) > 500:
            raise InvalidFieldException("merchant_params: Invalid Size, Size Must Be merchant_params <= 100")

    def get_merchant_params(self) -> List[Tuple[str, str]]:
        return self.__merchantParams

    def set_merchant_param(self, key: str, value: str) -> None:
        if self.__merchantParams is None:
            self.__merchantParams = []
        self.__merchantParams.append((key, value))
        if len(GeneralUtils.merchant_params_query(self.__merchantParams)) > 500:
            raise InvalidFieldException("merchant_params: Invalid Size, Size Must Be merchant_params <= 100")

    def set_credentials(self, credentials: Credentials) -> None:
        self.__merchantId = credentials.get_merchant_id()
        self.__productId = credentials.get_product_id()
        self.__apiVersion = credentials.get_api_version()

    def is_missing_field(self) -> Tuple[bool, str]:
        if self.__apiVersion < 0:
            return True, "api_version"

        mandatory_fields = {
            "merchantId": self.__merchantId,
            "productId": self.__productId,
            "merchantTransactionId": self.__merchantTransactionId,
            "amount": self.__amount,
            "currency": self.__currency,
            "country": self.__country,
            "paymentSolution": self.__paymentSolution,
            "customerId": self.__customerId,
            "operationType": self.__operationType,
            "statusURL": self.__statusURL,
            "successURL": self.__successURL,
            "errorURL": self.__errorURL,
            "cancelURL": self.__cancelURL,
            "awaitingURL": self.__awaitingURL,
            "prepayToken": self.__prepayToken
        }

        return GeneralUtils.contains_null(mandatory_fields)

    def check_credentials(self, credentials: Credentials) -> Tuple[bool, str]:
        if credentials.get_api_version() < 0:
            return True, "apiVersion"

        mandatory_fields = {
            "merchant_id": credentials.get_merchant_id(),
            "product_id": credentials.get_product_id(),
            "merchant_key": credentials.get_merchant_key(),
            "environment": credentials.get_environment()
        }

        return GeneralUtils.contains_null(mandatory_fields)

    def to_dict(self):
        dict_with_none = {
            "merchantId": self.__merchantId,
            "apiVersion": self.__apiVersion,
            "paymentSolution": self.__paymentSolution.value if self.__paymentSolution is not None else None,
            "operationType": self.__operationType.value if self.__operationType is not None else None,
            "merchantTransactionId": self.__merchantTransactionId,
            "amount": self.__amount,
            "currency": self.__currency.value if self.__currency is not None else None,
            "country": self.__country.value if self.__country is not None else None,
            "customerId": self.__customerId,
            "statusURL": self.__statusURL,
            "successURL": self.__successURL,
            "errorURL": self.__errorURL,
            "cancelURL": self.__cancelURL,
            "awaitingURL": self.__awaitingURL,
            "productId": self.__productId,
            "language": self.__language.value if self.__language is not None else None,
            "referenceId": self.__referenceId,
            "merchantParams": self.__merchantParams,
            "forceTokenRequest": self.__forceTokenRequest,
            "printReceipt": self.__printReceipt,
            "type": self.__type.value if self.__type is not None else None,
            "autoCapture": self.__autoCapture,
            "description": self.__description,
        }

        return {k: v for k, v in dict_with_none.items() if v is not None}
