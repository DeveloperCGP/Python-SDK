import json

from sdk.adapters.network_adapter import NetworkAdapter
from sdk.enums.endpoints import Endpoints
from sdk.enums.environment import Environment
from sdk.enums.error import Error
from sdk.enums.response_codes import ResponseCodes
from sdk.exceptions.field_exception import MissingFieldException
from sdk.models.credentials import Credentials
from sdk.models.requests.quix_hosted.hosted_quix_accommodation import HostedQuixAccommodation
from sdk.models.requests.quix_hosted.hosted_quix_flight import HostedQuixFlight
from sdk.models.requests.quix_hosted.hosted_quix_item import HostedQuixItem
from sdk.models.requests.quix_hosted.hosted_quix_service import HostedQuixService
from sdk.models.responses.payment_response import PaymentResponse
from sdk.utils.custom_encoder import CustomEncoder
from sdk.utils.general_utils import GeneralUtils
from sdk.utils.hex_utils import HexUtils
from sdk.utils.security_utils import SecurityUtils


class HostedQuixPaymentAdapter:

    def __init__(self, credentials: Credentials = None):
        self.__credentials = credentials
        self.__network_adapter = NetworkAdapter()

    def set_credentials(self, credentials: Credentials):
        self.__credentials = credentials

    def send_hosted_quix_service_request(self, hosted_quix_service: HostedQuixService) -> PaymentResponse:
        is_missing_cred = hosted_quix_service.check_credentials(self.__credentials)
        if is_missing_cred[0]:
            raise MissingFieldException(is_missing_cred[1], True)

        endpoint = Endpoints.HOSTED_ENDPOINT_PROD.value \
            if self.__credentials.get_environment() == Environment.PRODUCTION else Endpoints.HOSTED_ENDPOINT_STG.value

        hosted_quix_service.set_credentials(self.__credentials)

        is_missing_field = hosted_quix_service.is_missing_field()
        if is_missing_field[0]:
            raise MissingFieldException(is_missing_field[1], False)

        http_query = GeneralUtils.generate_query(hosted_quix_service)
        json_object = json.dumps(hosted_quix_service.get_pay_sol_extended_data(), cls=CustomEncoder)
        http_query += f"&paysolExtendedData={json_object}"
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
            "merchantId": str(hosted_quix_service.get_merchant_id()),
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
                result.set_redirect_url(response[1])
            else:
                error_message = f"status code is {response[0]}" if response[1] is None or len(response[1]) else \
                    response[1]
                result.set_is_error(True)
                result.set_error(
                    Error.CLIENT_ERROR if ResponseCodes.is_client_error(response[0]) else Error.SERVER_ERROR)
                result.set_error_message(error_message)

        return result

    def send_hosted_quix_flight_request(self, hosted_quix_flight: HostedQuixFlight) -> PaymentResponse:
        is_missing_cred = hosted_quix_flight.check_credentials(self.__credentials)
        if is_missing_cred[0]:
            raise MissingFieldException(is_missing_cred[1], True)

        endpoint = Endpoints.HOSTED_ENDPOINT_PROD.value \
            if self.__credentials.get_environment() == Environment.PRODUCTION else Endpoints.HOSTED_ENDPOINT_STG.value

        hosted_quix_flight.set_credentials(self.__credentials)

        is_missing_field = hosted_quix_flight.is_missing_field()
        if is_missing_field[0]:
            raise MissingFieldException(is_missing_field[1], False)

        http_query = GeneralUtils.generate_query(hosted_quix_flight)
        json_object = json.dumps(hosted_quix_flight.get_pay_sol_extended_data(), cls=CustomEncoder)
        http_query += f"&paysolExtendedData={json_object}"
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
            "merchantId": str(hosted_quix_flight.get_merchant_id()),
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
                result.set_redirect_url(response[1])
            else:
                error_message = f"status code is {response[0]}" if response[1] is None or len(response[1]) else \
                    response[1]
                result.set_is_error(True)
                result.set_error(
                    Error.CLIENT_ERROR if ResponseCodes.is_client_error(response[0]) else Error.SERVER_ERROR)
                result.set_error_message(error_message)

        return result

    def send_hosted_quix_accommodation_request(self,
                                               hosted_quix_accommodation: HostedQuixAccommodation) -> PaymentResponse:
        is_missing_cred = hosted_quix_accommodation.check_credentials(self.__credentials)
        if is_missing_cred[0]:
            raise MissingFieldException(is_missing_cred[1], True)

        endpoint = Endpoints.HOSTED_ENDPOINT_PROD.value \
            if self.__credentials.get_environment() == Environment.PRODUCTION else Endpoints.HOSTED_ENDPOINT_STG.value

        hosted_quix_accommodation.set_credentials(self.__credentials)

        is_missing_field = hosted_quix_accommodation.is_missing_field()
        if is_missing_field[0]:
            raise MissingFieldException(is_missing_field[1], False)

        http_query = GeneralUtils.generate_query(hosted_quix_accommodation)
        json_object = json.dumps(hosted_quix_accommodation.get_pay_sol_extended_data(), cls=CustomEncoder)
        http_query += f"&paysolExtendedData={json_object}"
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
            "merchantId": str(hosted_quix_accommodation.get_merchant_id()),
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
                result.set_redirect_url(response[1])
            else:
                error_message = f"status code is {response[0]}" if response[1] is None or len(response[1]) else \
                    response[1]
                result.set_is_error(True)
                result.set_error(
                    Error.CLIENT_ERROR if ResponseCodes.is_client_error(response[0]) else Error.SERVER_ERROR)
                result.set_error_message(error_message)

        return result

    def send_hosted_quix_item_request(self, hosted_quix_item: HostedQuixItem) -> PaymentResponse:
        is_missing_cred = hosted_quix_item.check_credentials(self.__credentials)
        if is_missing_cred[0]:
            raise MissingFieldException(is_missing_cred[1], True)

        endpoint = Endpoints.HOSTED_ENDPOINT_PROD.value \
            if self.__credentials.get_environment() == Environment.PRODUCTION else Endpoints.HOSTED_ENDPOINT_STG.value

        hosted_quix_item.set_credentials(self.__credentials)

        is_missing_field = hosted_quix_item.is_missing_field()
        if is_missing_field[0]:
            raise MissingFieldException(is_missing_field[1], False)

        http_query = GeneralUtils.generate_query(hosted_quix_item)
        json_object = json.dumps(hosted_quix_item.get_pay_sol_extended_data(), cls=CustomEncoder)
        http_query += f"&paysolExtendedData={json_object}"
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
            "merchantId": str(hosted_quix_item.get_merchant_id()),
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
                result.set_redirect_url(response[1])
            else:
                error_message = f"status code is {response[0]}" if response[1] is None or len(response[1]) else \
                    response[1]
                result.set_is_error(True)
                result.set_error(
                    Error.CLIENT_ERROR if ResponseCodes.is_client_error(response[0]) else Error.SERVER_ERROR)
                result.set_error_message(error_message)

        return result
