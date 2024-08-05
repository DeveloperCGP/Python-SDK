import json

from sdk.adapters.network_adapter import NetworkAdapter
from sdk.adapters.notification_adapter import parse_notification
from sdk.enums.endpoints import Endpoints
from sdk.enums.environment import Environment
from sdk.enums.error import Error
from sdk.enums.response_codes import ResponseCodes
from sdk.exceptions.field_exception import MissingFieldException
from sdk.models.credentials import Credentials
from sdk.models.requests.quix_js.js_quix_accommodation import JSQuixAccommodation
from sdk.models.requests.quix_js.js_quix_flight import JSQuixFlight
from sdk.models.requests.quix_js.js_quix_item import JSQuixItem
from sdk.models.requests.quix_js.js_quix_service import JSQuixService
from sdk.models.responses.payment_response import PaymentResponse
from sdk.utils.custom_encoder import CustomEncoder
from sdk.utils.general_utils import GeneralUtils


class JSQuixPaymentAdapter:

    def __init__(self, credentials: Credentials = None):
        self.__credentials = credentials
        self.__network_adapter = NetworkAdapter()

    def set_credentials(self, credentials: Credentials):
        self.__credentials = credentials

    def send_js_quix_service_request(self, js_quix_service: JSQuixService) -> PaymentResponse:
        is_missing_cred = js_quix_service.check_credentials(self.__credentials)
        if is_missing_cred[0]:
            raise MissingFieldException(is_missing_cred[1], True)

        endpoint = Endpoints.CHARGE_ENDPOINT_PROD.value if self.__credentials.get_environment() == Environment.PRODUCTION else \
            Endpoints.CHARGE_ENDPOINT_STG.value

        js_quix_service.set_credentials(self.__credentials)

        is_missing_field = js_quix_service.is_missing_field()
        if is_missing_field[0]:
            raise MissingFieldException(is_missing_field[1], False)

        body = json.dumps(js_quix_service, cls=CustomEncoder)
        json_object = json.loads(body)
        del json_object["prepayToken"]
        json_object["paysolExtendedData"] = str(
            json.dumps(js_quix_service.get_pay_sol_extended_data(), cls=CustomEncoder))

        headers = {
            "prepayToken": js_quix_service.get_prepay_token(),
            "apiVersion": str(self.__credentials.get_api_version())
        }

        response = self.__network_adapter.send_request(
            headers=headers,
            query_parameters=None,
            json=json_object,
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
                if response[1] is not None:
                    result.set_raw_response(response[1])
                result.set_error(
                    Error.CLIENT_ERROR if ResponseCodes.is_client_error(response[0]) else Error.SERVER_ERROR)
                result.set_error_message(error_message)

        return result

    def send_js_quix_flight_request(self, js_quix_flight: JSQuixFlight) -> PaymentResponse:
        is_missing_cred = js_quix_flight.check_credentials(self.__credentials)
        if is_missing_cred[0]:
            raise MissingFieldException(is_missing_cred[1], True)

        endpoint = Endpoints.CHARGE_ENDPOINT_PROD.value if self.__credentials.get_environment() == Environment.PRODUCTION else \
            Endpoints.CHARGE_ENDPOINT_STG.value

        js_quix_flight.set_credentials(self.__credentials)

        is_missing_field = js_quix_flight.is_missing_field()
        if is_missing_field[0]:
            raise MissingFieldException(is_missing_field[1], False)

        body = json.dumps(js_quix_flight, cls=CustomEncoder)
        json_object = json.loads(body)
        del json_object["prepayToken"]
        json_object["paysolExtendedData"] = str(
            json.dumps(js_quix_flight.get_pay_sol_extended_data(), cls=CustomEncoder))

        headers = {
            "prepayToken": js_quix_flight.get_prepay_token(),
            "apiVersion": str(self.__credentials.get_api_version())
        }

        response = self.__network_adapter.send_request(
            headers=headers,
            query_parameters=None,
            json=json_object,
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
                if response[1] is not None:
                    result.set_raw_response(response[1])
                result.set_error(
                    Error.CLIENT_ERROR if ResponseCodes.is_client_error(response[0]) else Error.SERVER_ERROR)
                result.set_error_message(error_message)

        return result

    def send_js_quix_accommodation_request(self, js_quix_accommodation: JSQuixAccommodation) -> PaymentResponse:
        is_missing_cred = js_quix_accommodation.check_credentials(self.__credentials)
        if is_missing_cred[0]:
            raise MissingFieldException(is_missing_cred[1], True)

        endpoint = Endpoints.CHARGE_ENDPOINT_PROD.value \
            if self.__credentials.get_environment() == Environment.PRODUCTION else \
            Endpoints.CHARGE_ENDPOINT_STG.value

        js_quix_accommodation.set_credentials(self.__credentials)

        is_missing_field = js_quix_accommodation.is_missing_field()
        if is_missing_field[0]:
            raise MissingFieldException(is_missing_field[1], False)

        for index, val in enumerate(js_quix_accommodation.get_pay_sol_extended_data().get_cart().get_items()):
            checkin_date = val.get_article().get_checkin_date()
            checkout_date = val.get_article().get_checkout_date()
            if ':' in checkin_date:
                js_quix_accommodation.get_pay_sol_extended_data() \
                    .get_cart().get_items()[index].get_article() \
                    .set_checkin_date(GeneralUtils.encode_url(checkin_date, False))
            if ':' in checkout_date:
                js_quix_accommodation.get_pay_sol_extended_data() \
                    .get_cart().get_items()[index].get_article() \
                    .set_checkout_date(GeneralUtils.encode_url(checkout_date, False))

        body = json.dumps(js_quix_accommodation, cls=CustomEncoder)
        json_object = json.loads(body)
        del json_object["prepayToken"]
        json_object["paysolExtendedData"] = str(json.dumps(
            js_quix_accommodation.get_pay_sol_extended_data(),
            cls=CustomEncoder
        ))

        headers = {
            "prepayToken": js_quix_accommodation.get_prepay_token(),
            "apiVersion": str(self.__credentials.get_api_version())
        }

        response = self.__network_adapter.send_request(
            headers=headers,
            query_parameters=None,
            json=json_object,
            url=endpoint
        )
        print(response)

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
                if response[1] is not None:
                    result.set_raw_response(response[1])
                result.set_error(
                    Error.CLIENT_ERROR if ResponseCodes.is_client_error(response[0]) else Error.SERVER_ERROR)
                result.set_error_message(error_message)

        return result

    def send_js_quix_item_request(self, js_quix_item: JSQuixItem) -> PaymentResponse:
        is_missing_cred = js_quix_item.check_credentials(self.__credentials)
        if is_missing_cred[0]:
            raise MissingFieldException(is_missing_cred[1], True)

        endpoint = Endpoints.CHARGE_ENDPOINT_PROD.value if self.__credentials.get_environment() == Environment.PRODUCTION else \
            Endpoints.CHARGE_ENDPOINT_STG.value

        js_quix_item.set_credentials(self.__credentials)

        is_missing_field = js_quix_item.is_missing_field()
        if is_missing_field[0]:
            raise MissingFieldException(is_missing_field[1], False)

        body = json.dumps(js_quix_item, cls=CustomEncoder)
        json_object = json.loads(body)
        del json_object["prepayToken"]
        json_object["paysolExtendedData"] = str(json.dumps(js_quix_item.get_pay_sol_extended_data(), cls=CustomEncoder))

        headers = {
            "prepayToken": js_quix_item.get_prepay_token(),
            "apiVersion": str(self.__credentials.get_api_version())
        }

        response = self.__network_adapter.send_request(
            headers=headers,
            query_parameters=None,
            json=json_object,
            url=endpoint
        )
        print(response)
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
                if response[1] is not None:
                    result.set_raw_response(response[1])
                result.set_error(
                    Error.CLIENT_ERROR if ResponseCodes.is_client_error(response[0]) else Error.SERVER_ERROR)
                result.set_error_message(error_message)

        return result
