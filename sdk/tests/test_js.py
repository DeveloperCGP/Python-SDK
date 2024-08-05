import os

import pytest

from sdk.adapters.js_payment_adapter import JSPaymentAdapter
from sdk.adapters.network_adapter import NetworkAdapter
from sdk.enums.country_code import CountryCodeAlpha2
from sdk.enums.currency import Currency
from sdk.enums.endpoints import Endpoints
from sdk.enums.environment import Environment
from sdk.enums.operation_types import OperationTypes
from sdk.enums.payment_recurring_type import PaymentRecurringType
from sdk.enums.payment_solutions import PaymentSolutions
from sdk.exceptions.field_exception import MissingFieldException
from sdk.models.credentials import Credentials
from sdk.models.requests.js.js_authorization_request import JSAuthorizationRequest
from sdk.models.requests.js.js_charge import JSCharge
from sdk.models.requests.js.js_payment_recurrent_initial import JSPaymentRecurrentInitial

# Mock configurations
mock_configurations = {
    "merchantId": "111222",
    "merchantPassword": "1234567890123456",
    "merchantKey": "35354a8e-ce22-40e1-863a-e58a8e53488e",
    "productId": "11111111",
    "statusUrl": "https://test.com",
    "baseURL": "https://test.com",
    "successUrl": "/success",
    "errorUrl": "/error",
    "awaitingUrl": "/awaiting",
    "cancelUrl": "/cancel"
}


@pytest.fixture
def setup_credentials():
    credentials = Credentials()
    credentials.set_merchant_id(mock_configurations["merchantId"])
    credentials.set_merchant_pass(mock_configurations["merchantPassword"])
    credentials.set_merchant_key(mock_configurations["merchantKey"])
    credentials.set_environment(Environment.STAGING)
    credentials.set_product_id(mock_configurations["productId"])
    credentials.set_api_version(5)
    return credentials


def read_xml_content(file_name):
    # Get the directory of the current file (test_notifications.py)
    current_file_directory = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the notifications directory relative to the current file
    xml_file_path = os.path.join(current_file_directory, 'notifications', file_name)

    if not os.path.exists(xml_file_path):
        raise FileNotFoundError(f"The file {xml_file_path} was not found.")

    with open(xml_file_path, 'r') as file:
        return file.read()


def test_send_charge_request_success(setup_credentials, mocker):
    # Mock the network adapter send_request method
    mock_send_request = mocker.patch.object(NetworkAdapter, 'send_request',
                                            return_value=(200, read_xml_content('js_charge.json')))

    # Create the HostedPaymentRedirection object
    request = JSCharge()
    request.set_amount("30")
    request.set_prepay_token("45357b66-8f04-4276-84f4-d35c885bde8e")
    request.set_country(CountryCodeAlpha2.ES)
    request.set_customer_id("55")
    request.set_currency(Currency.EUR)
    request.set_operation_type(OperationTypes.DEBIT)
    request.set_payment_solution(PaymentSolutions.creditcards)
    request.set_status_url("https://test.com/status")
    request.set_success_url("https://test.com/success")
    request.set_error_url("https://test.com/fail")
    request.set_awaiting_url("https://test.com/await")
    request.set_cancel_url("https://test.com/cancel")

    # Create the adapter and call the method
    adapter = JSPaymentAdapter(setup_credentials)
    result = adapter.send_js_charge_request(request)

    # Check the response
    redirect_url = result.get_notification().get_redirect_url()
    assert redirect_url == ("https://checkout.stg-eu-west3.epgint.com/EPGCheckout/rest/online/3dsv2/redirect?"
                            "action=gatherdevice&params=eyJ0aHJlZURTdjJUb2tlbiI6ImNjNWM1ODJjLWJiOTgtNGIyNS04Nj"
                            "A5LTZkZDI2YzM3MDgwNSIsInRocmVlRFNNZXRob2RVcmwiOiJodHRwczovL21vY2stZHMuc3RnLWV1LXd"
                            "lc3QzLmVwZ2ludC5jb20vcHVibGljL21ldGhvZC1kYXRhLyIsInRocmVlRFNNZXRob2REYXRhIjoiZXlKM"
                            "GFISmxaVVJUVTJWeWRtVnlWSEpoYm5OSlJDSTZJbU5qTldNMU9ESmpMV0ppT1RndE5HSXlOUzA0TmpBNUx"
                            "UWmtaREkyWXpNM01EZ3dOU0lzSUNKMGFISmxaVVJUVFdWMGFHOWtUbTkwYVdacFkyRjBhVzl1VlZKTUlq"
                            "b2dJbWgwZEhCek9pOHZZMmhsWTJ0dmRYUXVjM1JuTFdWMUxYZGxjM1F6TG1Wd1oybHVkQzVqYjIwdlJW"
                            "QkhRMmhsWTJ0dmRYUXZZMkZzYkdKaFkyc3ZaMkYwYUdWeVJHVjJhV05sVG05MGFXWnBZMkYwYVc5dUwz"
                            "QmhlWE52YkM4elpITjJNaTh4TURJek1ESTJJbjA9IiwiYnJhbmQiOiJWSVNBIiwicmVzdW1lQXV0aGVud"
                            "GljYXRpb24iOiJodHRwczovL2NoZWNrb3V0LnN0Zy1ldS13ZXN0My5lcGdpbnQuY29tL0VQR0NoZWNrb3V0"
                            "L3JldHVybnVybC9mcmljdGlvbmxlc3MvcGF5c29sLzNkc3YyLzEwMjMwMjY/dGhyZWVEU3YyVG9rZW49Y2M"
                            "1YzU4MmMtYmI5OC00YjI1LTg2MDktNmRkMjZjMzcwODA1IiwicmVuZGVyQ2FzaGllckxvY2F0aW9uIjoiaH"
                            "R0cHM6Ly9lcGdqcy1yZW5kZXJjYXNoaWVyLXN0Zy5lYXN5cGF5bWVudGdhdGV3YXkuY29tIiwiY2hhbGxlb"
                            "mdlV2luZG93c1NpemUiOiIwNSJ9")
    # Capture the network call arguments
    mock_send_request.assert_called_once()
    call_args = mock_send_request.call_args
    json = call_args[1]['json']
    url = call_args[1]['url']
    # Verify the network call arguments
    assert json["merchantId"] == "111222"
    assert url == Endpoints.CHARGE_ENDPOINT_STG.value  # Change this to the correct endpoint


@pytest.mark.parametrize("missing_field", [
    "amount",
    "prepayToken",
    "country",
    "customerId",
    "currency",
    "operationType",
    "paymentSolution",
    "statusURL",
    "successURL",
    "errorURL",
    "awaitingURL",
    "cancelURL",
])
def test_missing_mandatory_field_throws_exception_js_charge(setup_credentials, missing_field):
    # Create the JSCharge object with all mandatory fields set
    request = JSCharge()
    request.set_amount("30")
    request.set_prepay_token("45357b66-8f04-4276-84f4-d35c885bde8e")
    request.set_country(CountryCodeAlpha2.ES)
    request.set_customer_id("55")
    request.set_currency(Currency.EUR)
    request.set_operation_type(OperationTypes.DEBIT)
    request.set_payment_solution(PaymentSolutions.creditcards)
    request.set_status_url("https://test.com/status")
    request.set_success_url("https://test.com/success")
    request.set_error_url("https://test.com/fail")
    request.set_awaiting_url("https://test.com/await")
    request.set_cancel_url("https://test.com/cancel")

    # Remove the specified mandatory field by setting it to None using setattr
    setattr(request, f"_JSCharge__{missing_field}", None)

    # Create the adapter
    adapter = JSPaymentAdapter(setup_credentials)

    # Assert that MissingFieldException is raised with the expected message when the request is sent
    with pytest.raises(MissingFieldException) as exc_info:
        adapter.send_js_charge_request(request)

    assert str(exc_info.value) == f"Missing {missing_field}"


def test_send_charge_recurring_request_success(setup_credentials, mocker):
    # Mock the network adapter send_request method
    mock_send_request = mocker.patch.object(NetworkAdapter, 'send_request',
                                            return_value=(200, read_xml_content('js_charge.json')))

    # Create the HostedPaymentRedirection object
    request = JSPaymentRecurrentInitial()
    request.set_amount("30")
    request.set_prepay_token("45357b66-8f04-4276-84f4-d35c885bde8e")
    request.set_country(CountryCodeAlpha2.ES)
    request.set_customer_id("55")
    request.set_currency(Currency.EUR)
    request.set_operation_type(OperationTypes.DEBIT)
    request.set_payment_solution(PaymentSolutions.creditcards)
    request.set_status_url("https://test.com/status")
    request.set_success_url("https://test.com/success")
    request.set_error_url("https://test.com/fail")
    request.set_awaiting_url("https://test.com/await")
    request.set_cancel_url("https://test.com/cancel")
    request.set_payment_recurring_type(PaymentRecurringType.newSubscription)

    # Create the adapter and call the method
    adapter = JSPaymentAdapter(setup_credentials)
    result = adapter.send_js_payment_recurrent_initial(request)

    # Check the response
    redirect_url = result.get_notification().get_redirect_url()
    assert redirect_url == ("https://checkout.stg-eu-west3.epgint.com/EPGCheckout/rest/online/3dsv2/redirect?"
                            "action=gatherdevice&params=eyJ0aHJlZURTdjJUb2tlbiI6ImNjNWM1ODJjLWJiOTgtNGIyNS04N"
                            "jA5LTZkZDI2YzM3MDgwNSIsInRocmVlRFNNZXRob2RVcmwiOiJodHRwczovL21vY2stZHMuc3RnLWV1LX"
                            "dlc3QzLmVwZ2ludC5jb20vcHVibGljL21ldGhvZC1kYXRhLyIsInRocmVlRFNNZXRob2REYXRhIjoiZXl"
                            "KMGFISmxaVVJUVTJWeWRtVnlWSEpoYm5OSlJDSTZJbU5qTldNMU9ESmpMV0ppT1RndE5HSXlOUzA0TmpB"
                            "NUxUWmtaREkyWXpNM01EZ3dOU0lzSUNKMGFISmxaVVJUVFdWMGFHOWtUbTkwYVdacFkyRjBhVzl1VlZKT"
                            "Ulqb2dJbWgwZEhCek9pOHZZMmhsWTJ0dmRYUXVjM1JuTFdWMUxYZGxjM1F6TG1Wd1oybHVkQzVqYjIwdlJW"
                            "QkhRMmhsWTJ0dmRYUXZZMkZzYkdKaFkyc3ZaMkYwYUdWeVJHVjJhV05sVG05MGFXWnBZMkYwYVc5dUwzQmh"
                            "lWE52YkM4elpITjJNaTh4TURJek1ESTJJbjA9IiwiYnJhbmQiOiJWSVNBIiwicmVzdW1lQXV0aGVudGljYXR"
                            "pb24iOiJodHRwczovL2NoZWNrb3V0LnN0Zy1ldS13ZXN0My5lcGdpbnQuY29tL0VQR0NoZWNrb3V0L3JldHV"
                            "ybnVybC9mcmljdGlvbmxlc3MvcGF5c29sLzNkc3YyLzEwMjMwMjY/dGhyZWVEU3YyVG9rZW49Y2M1YzU4MmM"
                            "tYmI5OC00YjI1LTg2MDktNmRkMjZjMzcwODA1IiwicmVuZGVyQ2FzaGllckxvY2F0aW9uIjoiaHR0cHM6Ly9"
                            "lcGdqcy1yZW5kZXJjYXNoaWVyLXN0Zy5lYXN5cGF5bWVudGdhdGV3YXkuY29tIiwiY2hhbGxlbmdlV2luZG9"
                            "3c1NpemUiOiIwNSJ9")
    # Capture the network call arguments
    mock_send_request.assert_called_once()
    call_args = mock_send_request.call_args
    json = call_args[1]['json']
    url = call_args[1]['url']
    # Verify the network call arguments
    assert json["merchantId"] == "111222"
    assert url == Endpoints.CHARGE_ENDPOINT_STG.value  # Change this to the correct endpoint


def test_send_auth_request_success(setup_credentials, mocker):
    # Mock the network adapter send_request method
    mock_send_request = mocker.patch.object(NetworkAdapter, 'send_request', return_value=(
        200, "{\"authToken\":\"96d1e757-b3ba-474a-a4da-9c771585fbe5\"}"))

    request = JSAuthorizationRequest()
    request.set_country(CountryCodeAlpha2.ES)
    request.set_customer_id("55")
    request.set_currency(Currency.EUR)
    request.set_operation_type(OperationTypes.DEBIT)
    request.set_anonymous_customer(False)

    # Create the adapter and call the method
    adapter = JSPaymentAdapter(setup_credentials)
    result = adapter.send_js_authorization_request(request)

    # Check the response
    auth_token = result.get_auth_token()
    assert auth_token == "96d1e757-b3ba-474a-a4da-9c771585fbe5"
    # Capture the network call arguments
    mock_send_request.assert_called_once()
    call_args = mock_send_request.call_args
    json = call_args[1]['json']
    url = call_args[1]['url']
    # Verify the network call arguments
    assert json["merchantId"] == "111222"
    assert url == Endpoints.AUTH_ENDPOINT_STG.value  # Change this to the correct endpoint


@pytest.mark.parametrize("missing_field", [
    "country",
    "customerId",
    "currency",
    "operationType",
])
def test_missing_mandatory_field_throws_exception_js_authorization(setup_credentials, missing_field):
    # Create the JSAuthorizationRequest object with all mandatory fields set
    request = JSAuthorizationRequest()
    request.set_country(CountryCodeAlpha2.ES)
    request.set_customer_id("55")
    request.set_currency(Currency.EUR)
    request.set_operation_type(OperationTypes.DEBIT)
    request.set_anonymous_customer(False)

    # Remove the specified mandatory field by setting it to None using setattr
    setattr(request, f"_JSAuthorizationRequest__{missing_field}", None)

    # Create the adapter
    adapter = JSPaymentAdapter(setup_credentials)

    # Assert that MissingFieldException is raised with the expected message when the request is sent
    with pytest.raises(MissingFieldException) as exc_info:
        adapter.send_js_authorization_request(request)

    assert str(exc_info.value) == f"Missing {missing_field}"
