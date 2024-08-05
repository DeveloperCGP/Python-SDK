import json

from sdk.adapters.network_adapter import NetworkAdapter
from sdk.adapters.notification_adapter import parse_notification
from sdk.enums.endpoints import Endpoints
from sdk.enums.environment import Environment
from sdk.enums.error import Error
from sdk.enums.response_codes import ResponseCodes
from sdk.exceptions.field_exception import MissingFieldException
from sdk.models.credentials import Credentials
from sdk.models.requests.js.js_authorization_request import JSAuthorizationRequest
from sdk.models.requests.js.js_charge import JSCharge
from sdk.models.requests.js.js_payment_recurrent_initial import JSPaymentRecurrentInitial
from sdk.models.responses.js_authorization_response import JSAuthorizationResponse
from sdk.models.responses.payment_response import PaymentResponse
from sdk.utils.custom_encoder import CustomEncoder
from sdk.utils.general_utils import GeneralUtils


class JSPaymentAdapter:

    def __init__(self, credentials: Credentials = None):
        self.__credentials = credentials
        self.__network_adapter = NetworkAdapter()

    def set_credentials(self, credentials: Credentials):
        self.__credentials = credentials

    def send_js_authorization_request(self,
                                      js_authorization_request: JSAuthorizationRequest) -> JSAuthorizationResponse:
        is_missing_cred = js_authorization_request.check_credentials(self.__credentials)
        if is_missing_cred[0]:
            raise MissingFieldException(is_missing_cred[1], True)

        endpoint = Endpoints.AUTH_ENDPOINT_PROD.value \
            if self.__credentials.get_environment() == Environment.PRODUCTION else \
            Endpoints.AUTH_ENDPOINT_STG.value

        js_authorization_request.set_credentials(self.__credentials)

        is_missing_field = js_authorization_request.is_missing_field()
        if is_missing_field[0]:
            raise MissingFieldException(is_missing_field[1], False)

        body = json.dumps(js_authorization_request, cls=CustomEncoder)

        response = self.__network_adapter.send_request(
            headers=None,
            query_parameters=None,
            json=json.loads(body),
            url=endpoint
        )

        print(f"response = {response}")
        result = JSAuthorizationResponse()
        if isinstance(response[0], Error):
            result.set_is_error(True)
            result.set_error(response[0])
            result.set_error_message(response[1])
        else:
            if ResponseCodes.is_success(response[0]):
                result.set_is_error(False)
                json_response = json.loads(response[1])
                result.set_auth_token(json_response['authToken'])
            else:
                error_message = f"status code is {response[0]}" if response[1] is None or len(response[1]) else \
                    response[1]
                result.set_is_error(True)
                result.set_error(
                    Error.CLIENT_ERROR if ResponseCodes.is_client_error(response[0]) else Error.SERVER_ERROR)
                result.set_error_message(error_message)

        return result

    def send_js_charge_request(self, js_charge: JSCharge) -> PaymentResponse:
        is_missing_cred = js_charge.check_credentials(self.__credentials)
        if is_missing_cred[0]:
            raise MissingFieldException(is_missing_cred[1], True)

        endpoint = Endpoints.CAPTURE_ENDPOINT_PROD.value \
            if self.__credentials.get_environment() == Environment.PRODUCTION else \
            Endpoints.CHARGE_ENDPOINT_STG.value

        js_charge.set_credentials(self.__credentials)

        is_missing_field = js_charge.is_missing_field()
        if is_missing_field[0]:
            raise MissingFieldException(is_missing_field[1], False)

        body = json.dumps(js_charge, cls=CustomEncoder)
        body_json = json.loads(body)
        if "merchantParams" in body_json:
            body_json["merchantParams"] = GeneralUtils.merchant_params_query(js_charge.get_merchant_params())

        headers = {
            "prepayToken": js_charge.get_prepay_token(),
            "apiVersion": str(js_charge.get_api_version())
        }

        response = self.__network_adapter.send_request(
            headers=headers,
            query_parameters=None,
            json=body_json,
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

    def send_js_payment_recurrent_initial(self,
                                          js_payment_recurrent_initial: JSPaymentRecurrentInitial) -> PaymentResponse:
        is_missing_cred = js_payment_recurrent_initial.check_credentials(self.__credentials)
        if is_missing_cred[0]:
            raise MissingFieldException(is_missing_cred[1], True)

        endpoint = Endpoints.CAPTURE_ENDPOINT_PROD.value \
            if self.__credentials.get_environment() == Environment.PRODUCTION else \
            Endpoints.CHARGE_ENDPOINT_STG.value

        js_payment_recurrent_initial.set_credentials(self.__credentials)

        is_missing_field = js_payment_recurrent_initial.is_missing_field()
        if is_missing_field[0]:
            raise MissingFieldException(is_missing_field[1], False)

        body = json.dumps(js_payment_recurrent_initial, cls=CustomEncoder)
        body_json = json.loads(body)
        if "merchantParams" in body_json:
            body_json["merchantParams"] = GeneralUtils.merchant_params_query(
                js_payment_recurrent_initial.get_merchant_params()
            )

        headers = {
            "prepayToken": js_payment_recurrent_initial.get_prepay_token(),
            "apiVersion": str(js_payment_recurrent_initial.get_api_version())
        }

        response = self.__network_adapter.send_request(
            headers=headers,
            query_parameters=None,
            json=body_json,
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
