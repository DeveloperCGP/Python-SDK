from typing import Tuple

from sdk.enums.country_code import CountryCodeAlpha2
from sdk.enums.currency import Currency
from sdk.enums.language import Language
from sdk.enums.operation_types import OperationTypes
from sdk.enums.payment_solutions import PaymentSolutions
from sdk.exceptions.field_exception import InvalidFieldException
from sdk.models.credentials import Credentials
from sdk.utils.general_utils import GeneralUtils


class QuixHostedRequest:
    __paymentSolution: PaymentSolutions = None
    __currency: Currency = None
    __country: CountryCodeAlpha2 = None
    __customerCountry: CountryCodeAlpha2 = None
    __merchantId: str = None
    __productId: str = None
    __merchantTransactionId: str = None
    __amount: str = None
    __customerId: str = None
    __statusURL: str = None
    __successURL: str = None
    __errorURL: str = None
    __cancelURL: str = None
    __awaitingURL: str = None
    __firstName: str = None
    __lastName: str = None
    __customerEmail: str = None
    __customerNationalId: str = None
    __dob: str = None
    __ipAddress: str = None
    __operationType: OperationTypes = None
    __paymentMethod: str = None
    __telephone: str = None
    __language: Language = None

    def __init__(self):
        self.__paymentSolution = PaymentSolutions.quix
        self.__country = CountryCodeAlpha2.ES
        self.__currency = Currency.EUR
        self.__country = CountryCodeAlpha2.ES
        self.__customerCountry = CountryCodeAlpha2.ES
        self.__merchantTransactionId = GeneralUtils.generate_random_number()
        self.__operationType: OperationTypes = OperationTypes.DEBIT

    def get_currency(self) -> Currency:
        return self.__currency

    def get_amount(self) -> str:
        return self.__amount

    def set_amount(self, amount) -> None:
        parsed_amount = GeneralUtils.parse_amount(amount)
        if parsed_amount is None:
            raise InvalidFieldException("amount: Should Follow Format #.#### And Be Between 0 And 1000000")
        self.__amount = parsed_amount

    def get_country(self) -> CountryCodeAlpha2:
        return self.__country

    def get_customer_id(self) -> str:
        return self.__customerId

    def set_customer_id(self, customer_id: str) -> None:
        if customer_id is None or len(customer_id) == 0 or len(customer_id) > 80:
            raise InvalidFieldException("customer_id: Invalid Size, size must be (0 < customer_id <= 80)")
        self.__customerId = customer_id

    def get_merchant_id(self) -> str:
        return self.__merchantId

    def get_merchant_transaction_id(self) -> str:
        return self.__merchantTransactionId

    def set_merchant_transaction_id(self, merchant_transaction_id: str) -> None:
        if not merchant_transaction_id or len(merchant_transaction_id) > 45:
            raise InvalidFieldException(
                "merchant_transaction_id: Invalid Size, size must be (0 < merchant_transaction_id <= 45)")
        self.__merchantTransactionId = merchant_transaction_id

    def get_payment_solution(self) -> PaymentSolutions:
        return self.__paymentSolution

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
            raise InvalidFieldException("success_url")
        self.__successURL = success_url

    def get_awaiting_url(self) -> str:
        return self.__awaitingURL

    def set_awaiting_url(self, awaiting_url: str) -> None:
        if not GeneralUtils.is_valid_url(awaiting_url):
            raise InvalidFieldException("awaiting_url")
        self.__awaitingURL = awaiting_url

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

    def get_first_name(self) -> str:
        return self.__firstName

    def set_first_name(self, first_name: str) -> None:
        self.__firstName = first_name

    def get_last_name(self) -> str:
        return self.__lastName

    def set_last_name(self, last_name: str) -> None:
        self.__lastName = last_name

    def get_product_id(self) -> str:
        return self.__productId

    def get_customer_email(self) -> str:
        return self.__customerEmail

    def set_customer_email(self, customer_email: str) -> None:
        self.__customerEmail = customer_email

    def get_customer_country(self) -> CountryCodeAlpha2:
        return self.__customerCountry

    def get_dob(self) -> str:
        return self.__dob

    def set_dob(self, dob: str) -> None:
        self.__dob = dob

    def get_customer_national_id(self) -> str:
        return self.__customerNationalId

    def set_customer_national_id(self, customer_national_id: str) -> None:
        if len(customer_national_id) > 100:
            raise InvalidFieldException(
                "customer_national_id: Invalid Size, size must be (customer_national_id <= 100)")
        self.__customerNationalId = customer_national_id

    def get_ip_address(self) -> str:
        return self.__ipAddress

    def set_ip_address(self, ip_address: str) -> None:
        if len(ip_address) > 45 or not GeneralUtils.is_valid_ip(ip_address):
            raise InvalidFieldException("ip_address: must follow format IPv4 or IPv6 and max size is 45")
        self.__ipAddress = ip_address

    def get_operation_type(self) -> OperationTypes:
        return self.__operationType

    def set_operation_type(self, operation_type: OperationTypes) -> None:
        self.__operationType = operation_type

    def get_payment_method(self) -> str:
        return self.__paymentMethod

    def set_payment_method(self, payment_method: str) -> None:
        self.__paymentMethod = payment_method

    def get_telephone(self) -> str:
        return self.__telephone

    def set_telephone(self, telephone: str) -> None:
        if len(telephone) > 45:
            raise InvalidFieldException("telephone: Invalid Size, size must be (telephone <= 45)")
        self.__telephone = telephone

    def get_language(self) -> Language:
        return self.__language

    def set_language(self, language: Language) -> None:
        self.__language = language

    def set_credentials(self, credentials: Credentials) -> None:
        self.__merchantId = credentials.get_merchant_id()
        self.__productId = credentials.get_product_id()

    def is_missing_field(self):
        mandatory_fields = {
            "merchantId": self.__merchantId,
            "productId": self.__productId,
            "paymentSolution": self.__paymentSolution,
            "merchantTransactionId": self.__merchantTransactionId,
            "amount": self.__amount,
            "currency": self.__currency,
            "country": self.__country,
            "customerId": self.__customerId,
            "awaitingURL": self.__awaitingURL,
            "statusURL": self.__statusURL,
            "successURL": self.__successURL,
            "errorURL": self.__errorURL,
            "cancelURL": self.__cancelURL,
            "firstName": self.__firstName,
            "lastName": self.__lastName,
            "customerEmail": self.__customerEmail,
            "customerCountry": self.__customerCountry,
            "customerNationalId": self.__customerNationalId,
            "dob": self.__dob,
            "ipAddress": self.__ipAddress
        }

        return GeneralUtils.contains_null(mandatory_fields)

    def check_credentials(self, credentials: Credentials) -> Tuple[bool, str]:
        if credentials.get_api_version() < 0:
            return True, "api_version"
        mandatory_fields = {
            "merchant_id": credentials.get_merchant_id(),
            "product_id": credentials.get_product_id(),
            "environment": credentials.get_environment()
        }
        return GeneralUtils.contains_null(mandatory_fields)

    def to_dict(self):
        dict_with_none = {
            "paymentSolution": self.__paymentSolution,
            "currency": self.__currency,
            "country": self.__country,
            "customerCountry": self.__customerCountry,
            "merchantId": self.__merchantId,
            "productId": self.__productId,
            "merchantTransactionId": self.__merchantTransactionId,
            "amount": self.__amount,
            "customerId": self.__customerId,
            "statusURL": self.__statusURL,
            "successURL": self.__successURL,
            "errorURL": self.__errorURL,
            "cancelURL": self.__cancelURL,
            "awaitingURL": self.__awaitingURL,
            "firstName": self.__firstName,
            "lastName": self.__lastName,
            "customerEmail": self.__customerEmail,
            "customerNationalId": self.__customerNationalId,
            "dob": self.__dob,
            "ipAddress": self.__ipAddress,
            "operationType": self.__operationType,
            "paymentMethod": self.__paymentMethod,
            "telephone": self.__telephone,
            "language": self.__language,
        }
        return {k: v for k, v in dict_with_none.items() if v is not None}
