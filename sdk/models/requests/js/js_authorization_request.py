from dataclasses import dataclass
from typing import Tuple

from sdk.enums.country_code import CountryCodeAlpha2
from sdk.enums.currency import Currency
from sdk.enums.operation_types import OperationTypes
from sdk.exceptions.field_exception import InvalidFieldException
from sdk.models.credentials import Credentials
from sdk.utils.general_utils import GeneralUtils


@dataclass
class JSAuthorizationRequest:
    __merchantId: str = None
    __merchantKey: str = None
    __productId: str = None
    __currency: Currency = None
    __country: CountryCodeAlpha2 = None
    __customerId: str = None
    __operationType: OperationTypes = None
    __anonymousCustomer: bool = False

    def get_currency(self) -> Currency:
        return self.__currency

    def set_currency(self, currency: Currency) -> None:
        self.__currency = currency

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

    def get_operation_type(self) -> OperationTypes:
        return self.__operationType

    def set_operation_type(self, operation_type: OperationTypes) -> None:
        self.__operationType = operation_type

    def get_merchant_id(self) -> str:
        return self.__merchantId

    def get_merchant_key(self) -> str:
        return self.__merchantKey

    def is_anonymous_customer(self) -> bool:
        return self.__anonymousCustomer

    def set_anonymous_customer(self, anonymous_customer: bool) -> None:
        self.__anonymousCustomer = anonymous_customer

    def set_credentials(self, credentials: Credentials) -> None:
        self.__merchantId = credentials.get_merchant_id()
        self.__productId = credentials.get_product_id()
        self.__merchantKey = credentials.get_merchant_key()

    def is_missing_field(self) -> Tuple[bool, str]:
        mandatory_fields = {
            "merchantId": self.__merchantId,
            "productId": self.__productId,
            "merchantKey": self.__merchantKey,
            "currency": self.__currency,
            "country": self.__country,
            "customerId": self.__customerId,
            "operationType": self.__operationType
        }

        return GeneralUtils.contains_null(mandatory_fields)

    def check_credentials(self, credentials: Credentials) -> Tuple[bool, str]:
        if credentials.get_api_version() < 0:
            return True, "api_version"
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
            "merchantKey": self.__merchantKey,
            "productId": self.__productId,
            "currency": self.__currency,
            "country": self.__country,
            "customerId": self.__customerId,
            "operationType": self.__operationType,
            "anonymousCustomer": self.__anonymousCustomer,
        }

        return {k: v for k, v in dict_with_none.items() if v is not None}
