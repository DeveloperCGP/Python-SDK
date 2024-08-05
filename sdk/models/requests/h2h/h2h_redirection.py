from typing import List, Tuple, Optional

from sdk.enums.country_code import CountryCodeAlpha2
from sdk.enums.currency import Currency
from sdk.enums.h2h_operation_type import H2HOperationType
from sdk.enums.language import Language
from sdk.enums.payment_solutions import PaymentSolutions
from sdk.enums.transaction import TransactionType
from sdk.exceptions.field_exception import InvalidFieldException
from sdk.models.credentials import Credentials
from sdk.utils.general_utils import GeneralUtils


class H2HRedirection:
    __amount: str = None
    __country: CountryCodeAlpha2 = None
    __currency: Currency = None
    __customerId: str = None
    __merchantId: str = None
    __merchantTransactionId: str = None
    __paymentSolution: PaymentSolutions = None
    __chName: str = None
    __cardNumber: str = None
    __expDate: str = None
    __cvnNumber: str = None
    __cardNumberToken: str = None
    __statusURL: str = None
    __successURL: str = None
    __errorURL: str = None
    __cancelURL: str = None
    __awaitingURL: str = None
    __productId: str = None
    __operationType: H2HOperationType = None
    __forceTokenRequest: bool = None
    __language: Language = None
    __referenceId: str = None
    __printReceipt: bool = None
    __type: TransactionType = None
    __autoCapture: bool = None
    __merchantParams: List[Tuple[str, str]] = None

    def __init__(self):
        self.__merchantTransactionId = GeneralUtils.generate_random_number()
        self.__operationType = H2HOperationType.DEBIT
        self.__type = TransactionType.ECOM

    def get_amount(self):
        return self.__amount

    def set_amount(self, new_amount):
        parsed_amount = GeneralUtils.parse_amount(new_amount)
        if parsed_amount is None:
            raise InvalidFieldException("amount: Should Follow Format #.#### And Be Between 0 And 1000000")
        self.__amount = parsed_amount

    def set_country(self, new_country: CountryCodeAlpha2):
        self.__country = new_country

    def get_country(self):
        return self.__country

    def set_currency(self, new_currency: Currency):
        self.__currency = new_currency

    def get_currency(self):
        return self.__currency

    def get_customer_id(self):
        return self.__customerId

    def set_customer_id(self, new_customer_id: str):
        if new_customer_id is None or not new_customer_id or len(new_customer_id) > 80:
            raise InvalidFieldException("customerId: Invalid Size, size must be (0 < customerId <= 80)")
        self.__customerId = new_customer_id

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

    def get_ch_name(self):
        return self.__chName

    def set_ch_name(self, new_ch_name: str):
        if len(new_ch_name) > 100:
            raise InvalidFieldException("chName: Invalid Size, Size Must Be chName <= 100")
        self.__chName = new_ch_name

    def get_card_number(self):
        return self.__cardNumber

    def set_card_number(self, new_card_number: str):
        if len(new_card_number) > 19 or not GeneralUtils.check_luhn(new_card_number):
            raise InvalidFieldException("cardNumber")
        self.__cardNumber = new_card_number

    def get_exp_date(self):
        return self.__expDate

    def set_exp_date(self, new_exp_date: str):
        if not GeneralUtils.is_valid_exp_date(new_exp_date):
            raise InvalidFieldException("expDate: Should Be In Format MMYY")
        self.__expDate = new_exp_date

    def get_cvn_number(self):
        return self.__cvnNumber

    def set_cvn_number(self, new_cvn_number: str):
        if not new_cvn_number.isdigit() or len(new_cvn_number) < 3 or len(new_cvn_number) > 4:
            raise InvalidFieldException("cvnNumber: Should Be Numerical 3 to 4 Digits")
        self.__cvnNumber = new_cvn_number

    def get_card_number_token(self):
        return self.__cardNumberToken

    def set_card_number_token(self, new_card_number_token: str):
        if len(new_card_number_token) < 16 or len(new_card_number_token) > 20:
            raise InvalidFieldException("cardNumberToken: Invalid Size, Size Must Be 16 <= cardNumberToken <= 20")
        self.__cardNumberToken = new_card_number_token

    def get_status_url(self):
        return self.__statusURL

    def set_status_url(self, new_status_url: str):
        if not GeneralUtils.is_valid_url(new_status_url):
            raise InvalidFieldException("statusURL: Must be a valid url")
        self.__statusURL = new_status_url

    def get_success_url(self):
        return self.__successURL

    def set_success_url(self, new_success_url: str):
        if not GeneralUtils.is_valid_url(new_success_url):
            raise InvalidFieldException("successURL")
        self.__successURL = new_success_url

    def get_error_url(self):
        return self.__errorURL

    def set_error_url(self, new_error_url: str):
        if not GeneralUtils.is_valid_url(new_error_url):
            raise InvalidFieldException("errorURL")
        self.__errorURL = new_error_url

    def get_cancel_url(self):
        return self.__cancelURL

    def set_cancel_url(self, new_cancel_url: str):
        if not GeneralUtils.is_valid_url(new_cancel_url):
            raise InvalidFieldException("cancelURL")
        self.__cancelURL = new_cancel_url

    def get_awaiting_url(self):
        return self.__awaitingURL

    def set_awaiting_url(self, new_awaiting_url: str):
        if not GeneralUtils.is_valid_url(new_awaiting_url):
            raise InvalidFieldException("awaitingURL")
        self.__awaitingURL = new_awaiting_url

    def get_product_id(self):
        return self.__productId

    def get_operation_type(self):
        return self.__operationType

    def set_operation_type(self, new_operation_type: H2HOperationType):
        self.__operationType = new_operation_type

    def get_language(self):
        return self.__language

    def set_language(self, new_language: Language):
        self.__language = new_language

    def get_reference_id(self):
        return self.__referenceId

    def set_reference_id(self, new_reference_id: str):
        if len(new_reference_id) != 12:
            raise InvalidFieldException("referenceId: Invalid Size, size must be (referenceId = 12)")
        self.__referenceId = new_reference_id

    def get_print_receipt(self):
        return self.__printReceipt

    def set_print_receipt(self, new_print_receipt: bool):
        self.__printReceipt = new_print_receipt

    def get_type(self):
        return self.__type

    def set_type(self, new_type: TransactionType):
        self.__type = new_type

    def get_auto_capture(self):
        return self.__autoCapture

    def set_auto_capture(self, new_auto_capture: bool):
        self.__autoCapture = new_auto_capture

    def get_merchant_params(self):
        return self.__merchantParams

    def set_merchant_params(self, new_merchant_params: List[Tuple[str, str]]):
        if self.__merchantParams is None:
            self.__merchantParams = new_merchant_params
        else:
            self.__merchantParams.extend(new_merchant_params)
        if len(GeneralUtils.merchant_params_query(self.__merchantParams)) > 500:
            raise InvalidFieldException("merchantParams: Invalid Size, Size Must Be merchantParams <= 500")

    def set_merchant_param(self, new_merchant_param: Tuple[str, str]):
        if self.__merchantParams is None:
            self.__merchantParams = []
        self.__merchantParams.append(new_merchant_param)
        if len(GeneralUtils.merchant_params_query(self.__merchantParams)) > 500:
            raise InvalidFieldException("merchantParams: Invalid Size, Size Must Be merchantParams <= 500")

    def set_credentials(self, new_credentials: Credentials):
        if new_credentials is None:
            raise InvalidFieldException("credentials")
        self.__merchantId = new_credentials.get_merchant_id()
        self.__productId = new_credentials.get_product_id()

    def get_force_token_request(self):
        return self.__forceTokenRequest

    def set_force_token_request(self, force_token_request: bool):
        self.__forceTokenRequest = force_token_request

    def is_missing_field(self):
        mandatory_fields = {
            "amount": self.__amount,
            "country": self.__country,
            "currency": self.__currency,
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

        if self.__cardNumberToken is None:
            mandatory_fields["chName"] = self.__chName
            mandatory_fields["cardNumber"] = self.__cardNumber
            mandatory_fields["expDate"] = self.__expDate
            mandatory_fields["cvnNumber"] = self.__cvnNumber

        return GeneralUtils.contains_null(mandatory_fields)

    def check_credentials(self, credentials: Credentials) -> Tuple[bool, Optional[str]]:
        if credentials.get_api_version() < 0:
            return True, "apiVersion"

        mandatory_fields = {
            "merchantId": credentials.get_merchant_id(),
            "productId": credentials.get_product_id(),
            "merchantPass": credentials.get_merchant_pass(),
            "environment": credentials.get_environment().value
        }

        return GeneralUtils.contains_null(mandatory_fields)
