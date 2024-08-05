from sdk.adapters.network_adapter import NetworkAdapter
from sdk.adapters.notification_adapter import parse_notification
from sdk.enums.endpoints import Endpoints
from sdk.enums.environment import Environment
from sdk.enums.error import Error
from sdk.enums.response_codes import ResponseCodes
from sdk.exceptions.field_exception import MissingFieldException
from sdk.models.credentials import Credentials
from sdk.models.requests.h2h.h2h_payment_recurrent_initial import H2HPaymentRecurrentInitial
from sdk.models.requests.h2h.h2h_payment_recurrent_successive import H2HPaymentRecurrentSuccessive
from sdk.models.requests.h2h.h2h_pre_authorization import H2HPreAuthorization
from sdk.models.requests.h2h.h2h_pre_authorization_capture import H2HPreAuthorizationCapture
from sdk.models.requests.h2h.h2h_redirection import H2HRedirection
from sdk.models.requests.h2h.h2h_refund import H2HRefund
from sdk.models.requests.h2h.h2h_void import H2HVoid
from sdk.models.responses.payment_response import PaymentResponse
from sdk.utils.general_utils import GeneralUtils
from sdk.utils.hex_utils import HexUtils
from sdk.utils.security_utils import SecurityUtils


class H2HPaymentAdapter:

    def __init__(self, credentials: Credentials = None):
        self.__credentials = credentials
        self.__network_adapter = NetworkAdapter()

    def set_credentials(self, credentials: Credentials):
        self.__credentials = credentials

    def send_h2h_payment_request(self, h2h_redirection: H2HRedirection) -> PaymentResponse:
        is_missing_cred = h2h_redirection.check_credentials(self.__credentials)
        if is_missing_cred[0]:
            raise MissingFieldException(is_missing_cred[1], True)

        endpoint = Endpoints.H2H_ENDPOINT_PROD.value \
            if self.__credentials.get_environment() == Environment.PRODUCTION else Endpoints.H2H_ENDPOINT_STG.value

        h2h_redirection.set_credentials(self.__credentials)

        is_missing_field = h2h_redirection.is_missing_field()
        if is_missing_field[0]:
            raise MissingFieldException(is_missing_field[1], False)

        http_query = GeneralUtils.generate_query(h2h_redirection)
        final_query_parameter = GeneralUtils.encode_url(http_query)
        formatted_request = bytearray(final_query_parameter, 'utf-8')
        clear_iv = SecurityUtils.generate_iv()
        encrypted_request = SecurityUtils.cbc_encryption(
            data=formatted_request,
            key=bytearray(self.__credentials.get_merchant_pass(), 'utf-8'),
            iv=clear_iv
        )
        signature = SecurityUtils.hash256(formatted_request)
        headers = {
            "apiVersion": str(self.__credentials.get_api_version()),
            "encryptionMode": "CBC",
            "iv": SecurityUtils.base64_encode(clear_iv)
        }
        query_parameters = {
            "merchantId": str(h2h_redirection.get_merchant_id()),
            "encrypted": SecurityUtils.base64_encode(encrypted_request),
            "integrityCheck": HexUtils.bytes_to_hex(signature).lower()
        }

        response = self.__network_adapter.send_request(
            headers=headers,
            query_parameters=query_parameters,
            json=None,
            url=endpoint
        )

        result = PaymentResponse()
        if isinstance(response[0], Error):
            result.set_is_error(True)
            result.set_error(response[0])
            result.set_error_message(response[1])
        else:
            if ResponseCodes.is_success(response[0]):
                result.set_is_error(False)
                result.set_raw_response(response[1])
                result.set_notification(parse_notification(response[1]))
            else:
                error_message = f"status code is {response[0]}" if response[1] is None or len(response[1]) else \
                    response[1]
                result.set_is_error(True)
                result.set_error(
                    Error.CLIENT_ERROR if ResponseCodes.is_client_error(response[0]) else Error.SERVER_ERROR)
                result.set_error_message(error_message)

        return result

    def send_h2h_pre_authorization_request(self, h2h_pre_authorization: H2HPreAuthorization) -> PaymentResponse:
        is_missing_cred = h2h_pre_authorization.check_credentials(self.__credentials)
        if is_missing_cred[0]:
            raise MissingFieldException(is_missing_cred[1], True)

        endpoint = Endpoints.H2H_ENDPOINT_PROD.value \
            if self.__credentials.get_environment() == Environment.PRODUCTION else Endpoints.H2H_ENDPOINT_STG.value

        h2h_pre_authorization.set_credentials(self.__credentials)

        is_missing_field = h2h_pre_authorization.is_missing_field()
        if is_missing_field[0]:
            raise MissingFieldException(is_missing_field[1], False)

        http_query = GeneralUtils.generate_query(h2h_pre_authorization)
        final_query_parameter = GeneralUtils.encode_url(http_query)
        formatted_request = bytearray(final_query_parameter, 'utf-8')
        clear_iv = SecurityUtils.generate_iv()
        encrypted_request = SecurityUtils.cbc_encryption(
            data=formatted_request,
            key=bytearray(self.__credentials.get_merchant_pass(), 'utf-8'),
            iv=clear_iv
        )
        signature = SecurityUtils.hash256(formatted_request)
        headers = {
            "apiVersion": str(self.__credentials.get_api_version()),
            "encryptionMode": "CBC",
            "iv": SecurityUtils.base64_encode(clear_iv)
        }
        query_parameters = {
            "merchantId": str(h2h_pre_authorization.get_merchant_id()),
            "encrypted": SecurityUtils.base64_encode(encrypted_request),
            "integrityCheck": HexUtils.bytes_to_hex(signature).lower()
        }

        response = self.__network_adapter.send_request(
            headers=headers,
            query_parameters=query_parameters,
            json=None,
            url=endpoint
        )

        result = PaymentResponse()
        if isinstance(response[0], Error):
            result.set_is_error(True)
            result.set_error(response[0])
            result.set_error_message(response[1])
        else:
            if ResponseCodes.is_success(response[0]):
                result.set_is_error(False)
                result.set_raw_response(response[1])
                result.set_notification(parse_notification(response[1]))
            else:
                error_message = f"status code is {response[0]}" if response[1] is None or len(response[1]) else \
                    response[1]
                result.set_is_error(True)
                result.set_error(
                    Error.CLIENT_ERROR if ResponseCodes.is_client_error(response[0]) else Error.SERVER_ERROR)
                result.set_error_message(error_message)

        return result

    def send_h2h_pre_authorization_capture(
        self, h2h_pre_authorization_capture: H2HPreAuthorizationCapture
    ) -> PaymentResponse:
        is_missing_cred = h2h_pre_authorization_capture.check_credentials(self.__credentials)
        if is_missing_cred[0]:
            raise MissingFieldException(is_missing_cred[1], True)

        endpoint = Endpoints.CAPTURE_ENDPOINT_PROD.value \
            if self.__credentials.get_environment() == Environment.PRODUCTION else Endpoints.CAPTURE_ENDPOINT_STG.value

        h2h_pre_authorization_capture.set_credentials(self.__credentials)

        is_missing_field = h2h_pre_authorization_capture.is_missing_field()
        if is_missing_field[0]:
            raise MissingFieldException(is_missing_field[1], False)

        http_query = GeneralUtils.generate_query(h2h_pre_authorization_capture)
        final_query_parameter = GeneralUtils.encode_url(http_query)
        formatted_request = bytearray(final_query_parameter, 'utf-8')
        clear_iv = SecurityUtils.generate_iv()
        encrypted_request = SecurityUtils.cbc_encryption(
            data=formatted_request,
            key=bytearray(self.__credentials.get_merchant_pass(), 'utf-8'),
            iv=clear_iv
        )
        signature = SecurityUtils.hash256(formatted_request)
        headers = {
            "apiVersion": str(self.__credentials.get_api_version()),
            "encryptionMode": "CBC",
            "iv": SecurityUtils.base64_encode(clear_iv)
        }
        query_parameters = {
            "merchantId": str(h2h_pre_authorization_capture.get_merchant_id()),
            "encrypted": SecurityUtils.base64_encode(encrypted_request),
            "integrityCheck": HexUtils.bytes_to_hex(signature).lower()
        }

        response = self.__network_adapter.send_request(
            headers=headers,
            query_parameters=query_parameters,
            json=None,
            url=endpoint
        )

        result = PaymentResponse()
        if isinstance(response[0], Error):
            result.set_is_error(True)
            result.set_error(response[0])
            result.set_error_message(response[1])
        else:
            if ResponseCodes.is_success(response[0]):
                result.set_is_error(False)
                result.set_raw_response(response[1])
                result.set_notification(parse_notification(response[1]))
            else:
                error_message = f"status code is {response[0]}" if response[1] is None or len(response[1]) else \
                    response[1]
                result.set_is_error(True)
                result.set_error(
                    Error.CLIENT_ERROR if ResponseCodes.is_client_error(response[0]) else Error.SERVER_ERROR)
                result.set_error_message(error_message)

        return result

    def send_h2h_payment_recurrent_initial(
        self, h2h_payment_recurrent_initial: H2HPaymentRecurrentInitial
    ) -> PaymentResponse:
        is_missing_cred = h2h_payment_recurrent_initial.check_credentials(self.__credentials)
        if is_missing_cred[0]:
            raise MissingFieldException(is_missing_cred[1], True)

        endpoint = Endpoints.H2H_ENDPOINT_PROD.value \
            if self.__credentials.get_environment() == Environment.PRODUCTION else Endpoints.H2H_ENDPOINT_STG.value

        h2h_payment_recurrent_initial.set_credentials(self.__credentials)

        is_missing_field = h2h_payment_recurrent_initial.is_missing_field()
        if is_missing_field[0]:
            raise MissingFieldException(is_missing_field[1], False)

        http_query = GeneralUtils.generate_query(h2h_payment_recurrent_initial)
        print(f"HTTP Query: {http_query}")
        final_query_parameter = GeneralUtils.encode_url(http_query)
        formatted_request = bytearray(final_query_parameter, 'utf-8')
        clear_iv = SecurityUtils.generate_iv()
        encrypted_request = SecurityUtils.cbc_encryption(
            data=formatted_request,
            key=bytearray(self.__credentials.get_merchant_pass(), 'utf-8'),
            iv=clear_iv
        )
        signature = SecurityUtils.hash256(formatted_request)
        headers = {
            "apiVersion": str(self.__credentials.get_api_version()),
            "encryptionMode": "CBC",
            "iv": SecurityUtils.base64_encode(clear_iv)
        }
        query_parameters = {
            "merchantId": str(h2h_payment_recurrent_initial.get_merchant_id()),
            "encrypted": SecurityUtils.base64_encode(encrypted_request),
            "integrityCheck": HexUtils.bytes_to_hex(signature).lower()
        }

        response = self.__network_adapter.send_request(
            headers=headers,
            query_parameters=query_parameters,
            json=None,
            url=endpoint
        )

        result = PaymentResponse()
        if isinstance(response[0], Error):
            result.set_is_error(True)
            result.set_error(response[0])
            result.set_error_message(response[1])
        else:
            if ResponseCodes.is_success(response[0]):
                result.set_is_error(False)
                result.set_raw_response(response[1])
                result.set_notification(parse_notification(response[1]))
            else:
                error_message = f"status code is {response[0]}" if response[1] is None or len(response[1]) else \
                    response[1]
                result.set_is_error(True)
                result.set_error(
                    Error.CLIENT_ERROR if ResponseCodes.is_client_error(response[0]) else Error.SERVER_ERROR)
                result.set_error_message(error_message)

        return result

    def send_h2h_payment_recurrent_successive(
        self, h2h_payment_recurrent_successive: H2HPaymentRecurrentSuccessive
    ) -> PaymentResponse:
        is_missing_cred = h2h_payment_recurrent_successive.check_credentials(self.__credentials)
        if is_missing_cred[0]:
            raise MissingFieldException(is_missing_cred[1], True)

        endpoint = Endpoints.H2H_ENDPOINT_PROD.value \
            if self.__credentials.get_environment() == Environment.PRODUCTION else Endpoints.H2H_ENDPOINT_STG.value

        h2h_payment_recurrent_successive.set_credentials(self.__credentials)

        is_missing_field = h2h_payment_recurrent_successive.is_missing_field()
        if is_missing_field[0]:
            raise MissingFieldException(is_missing_field[1], False)

        http_query = GeneralUtils.generate_query(h2h_payment_recurrent_successive)
        final_query_parameter = GeneralUtils.encode_url(http_query)
        formatted_request = bytearray(final_query_parameter, 'utf-8')
        clear_iv = SecurityUtils.generate_iv()
        encrypted_request = SecurityUtils.cbc_encryption(
            data=formatted_request,
            key=bytearray(self.__credentials.get_merchant_pass(), 'utf-8'),
            iv=clear_iv
        )
        signature = SecurityUtils.hash256(formatted_request)
        headers = {
            "apiVersion": str(self.__credentials.get_api_version()),
            "encryptionMode": "CBC",
            "iv": SecurityUtils.base64_encode(clear_iv)
        }
        query_parameters = {
            "merchantId": str(h2h_payment_recurrent_successive.get_merchant_id()),
            "encrypted": SecurityUtils.base64_encode(encrypted_request),
            "integrityCheck": HexUtils.bytes_to_hex(signature).lower()
        }

        response = self.__network_adapter.send_request(
            headers=headers,
            query_parameters=query_parameters,
            json=None,
            url=endpoint
        )

        result = PaymentResponse()
        if isinstance(response[0], Error):
            result.set_is_error(True)
            result.set_error(response[0])
            result.set_error_message(response[1])
        else:
            if ResponseCodes.is_success(response[0]):
                result.set_is_error(False)
                result.set_raw_response(response[1])
                print(response[1])
            else:
                error_message = f"status code is {response[0]}" if response[1] is None or len(response[1]) else \
                    response[1]
                result.set_is_error(True)
                result.set_error(
                    Error.CLIENT_ERROR if ResponseCodes.is_client_error(response[0]) else Error.SERVER_ERROR)
                result.set_error_message(error_message)

        return result

    def send_h2h_void_request(self, h2h_void: H2HVoid) -> PaymentResponse:
        is_missing_cred = h2h_void.check_credentials(self.__credentials)
        if is_missing_cred[0]:
            raise MissingFieldException(is_missing_cred[1], True)

        endpoint = Endpoints.VOID_ENDPOINT_PROD.value \
            if self.__credentials.get_environment() == Environment.PRODUCTION else Endpoints.VOID_ENDPOINT_STG.value

        h2h_void.set_credentials(self.__credentials)

        is_missing_field = h2h_void.is_missing_field()
        if is_missing_field[0]:
            raise MissingFieldException(is_missing_field[1], False)

        http_query = GeneralUtils.generate_query(h2h_void)
        final_query_parameter = GeneralUtils.encode_url(http_query)
        formatted_request = bytearray(final_query_parameter, 'utf-8')
        clear_iv = SecurityUtils.generate_iv()
        encrypted_request = SecurityUtils.cbc_encryption(
            data=formatted_request,
            key=bytearray(self.__credentials.get_merchant_pass(), 'utf-8'),
            iv=clear_iv
        )
        signature = SecurityUtils.hash256(formatted_request)
        headers = {
            "apiVersion": str(self.__credentials.get_api_version()),
            "encryptionMode": "CBC",
            "iv": SecurityUtils.base64_encode(clear_iv)
        }
        query_parameters = {
            "merchantId": str(h2h_void.get_merchant_id()),
            "encrypted": SecurityUtils.base64_encode(encrypted_request),
            "integrityCheck": HexUtils.bytes_to_hex(signature).lower()
        }

        response = self.__network_adapter.send_request(
            headers=headers,
            query_parameters=query_parameters,
            json=None,
            url=endpoint
        )

        result = PaymentResponse()
        if isinstance(response[0], Error):
            result.set_is_error(True)
            result.set_error(response[0])
            result.set_error_message(response[1])
        else:
            if ResponseCodes.is_success(response[0]):
                result.set_is_error(False)
                result.set_raw_response(response[1])
                result.set_notification(parse_notification(response[1]))
            else:
                error_message = f"status code is {response[0]}" if response[1] is None or len(response[1]) else \
                    response[1]
                result.set_is_error(True)
                result.set_error(
                    Error.CLIENT_ERROR if ResponseCodes.is_client_error(response[0]) else Error.SERVER_ERROR)
                result.set_error_message(error_message)

        return result

    def send_h2h_refund_request(self, h2h_refund: H2HRefund) -> PaymentResponse:
        is_missing_cred = h2h_refund.check_credentials(self.__credentials)
        if is_missing_cred[0]:
            raise MissingFieldException(is_missing_cred[1], True)

        endpoint = Endpoints.REFUND_ENDPOINT_PROD.value \
            if self.__credentials.get_environment() == Environment.PRODUCTION else Endpoints.REFUND_ENDPOINT_STG.value

        h2h_refund.set_credentials(self.__credentials)

        is_missing_field = h2h_refund.is_missing_field()
        if is_missing_field[0]:
            raise MissingFieldException(is_missing_field[1], False)

        http_query = GeneralUtils.generate_query(h2h_refund)
        final_query_parameter = GeneralUtils.encode_url(http_query)
        formatted_request = bytearray(final_query_parameter, 'utf-8')
        clear_iv = SecurityUtils.generate_iv()
        encrypted_request = SecurityUtils.cbc_encryption(
            data=formatted_request,
            key=bytearray(self.__credentials.get_merchant_pass(), 'utf-8'),
            iv=clear_iv
        )
        signature = SecurityUtils.hash256(formatted_request)
        headers = {
            "apiVersion": str(self.__credentials.get_api_version()),
            "encryptionMode": "CBC",
            "iv": SecurityUtils.base64_encode(clear_iv)
        }
        query_parameters = {
            "merchantId": str(h2h_refund.get_merchant_id()),
            "encrypted": SecurityUtils.base64_encode(encrypted_request),
            "integrityCheck": HexUtils.bytes_to_hex(signature).lower()
        }

        response = self.__network_adapter.send_request(
            headers=headers,
            query_parameters=query_parameters,
            json=None,
            url=endpoint
        )

        result = PaymentResponse()
        if isinstance(response[0], Error):
            result.set_is_error(True)
            result.set_error(response[0])
            result.set_error_message(response[1])
        else:
            if ResponseCodes.is_success(response[0]):
                result.set_is_error(False)
                result.set_raw_response(response[1])
                result.set_notification(parse_notification(response[1]))
            else:
                error_message = f"status code is {response[0]}" if response[1] is None or len(response[1]) else \
                    response[1]
                result.set_is_error(True)
                result.set_error(
                    Error.CLIENT_ERROR if ResponseCodes.is_client_error(response[0]) else Error.SERVER_ERROR)
                result.set_error_message(error_message)

        return result
