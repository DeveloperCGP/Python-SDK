import pytest

from sdk.adapters.hosted_payment_adapter import HostedPaymentAdapter
from sdk.adapters.network_adapter import NetworkAdapter
from sdk.enums.country_code import CountryCodeAlpha2
from sdk.enums.currency import Currency
from sdk.enums.endpoints import Endpoints
from sdk.enums.environment import Environment
from sdk.enums.payment_recurring_type import PaymentRecurringType
from sdk.enums.payment_solutions import PaymentSolutions
from sdk.exceptions.field_exception import MissingFieldException
from sdk.models.credentials import Credentials
from sdk.models.requests.hosted.hosted_payment_recurrent_initial import HostedPaymentRecurrentInitial
from sdk.models.requests.hosted.hosted_payment_redirection import HostedPaymentRedirection
from sdk.utils.security_utils import SecurityUtils

# Mock configurations
mock_configurations = {
    "merchantId": "111222",
    "merchantPassword": "1234567890123456",
    "productId": "11111111",
    "statusUrl": "https://test.com",
    "baseURL": "https://test.com",
    "successUrl": "/success",
    "errorUrl": "/error",
    "awaitingUrl": "/awaiting",
    "cancelUrl": "/cancel"
}

fixed_iv = bytes([0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10])
encoded_iv = SecurityUtils.base64_encode(fixed_iv)  # Encode the fixed IV for verification


@pytest.fixture(autouse=True)
def setup_mock_security_utils(mocker):
    mocker.patch('sdk.utils.security_utils.SecurityUtils.generate_iv', return_value=fixed_iv)
    return mocker


@pytest.fixture
def setup_credentials():
    credentials = Credentials()
    credentials.set_merchant_id(mock_configurations["merchantId"])
    credentials.set_merchant_pass(mock_configurations["merchantPassword"])
    credentials.set_environment(Environment.STAGING)
    credentials.set_product_id(mock_configurations["productId"])
    credentials.set_api_version(5)
    return credentials


def test_send_hosted_returns_redirect_url_on_success(setup_credentials, mocker):
    # Mock the network adapter send_request method
    mock_send_request = mocker.patch.object(NetworkAdapter, 'send_request', return_value=(200, "http://redirect.url"))

    # Create the HostedPaymentRedirection object
    hosted_payment_redirection = HostedPaymentRedirection()
    hosted_payment_redirection.set_amount("50")
    hosted_payment_redirection.set_currency(Currency.EUR)
    hosted_payment_redirection.set_country(CountryCodeAlpha2.ES)
    hosted_payment_redirection.set_customer_id("903")
    hosted_payment_redirection.set_merchant_transaction_id("3123123")
    hosted_payment_redirection.set_payment_solution(PaymentSolutions.creditcards)
    hosted_payment_redirection.set_status_url(mock_configurations["statusUrl"])
    hosted_payment_redirection.set_success_url(mock_configurations["baseURL"] + mock_configurations["successUrl"])
    hosted_payment_redirection.set_error_url(mock_configurations["baseURL"] + mock_configurations["errorUrl"])
    hosted_payment_redirection.set_awaiting_url(mock_configurations["baseURL"] + mock_configurations["awaitingUrl"])
    hosted_payment_redirection.set_cancel_url(mock_configurations["baseURL"] + mock_configurations["cancelUrl"])
    hosted_payment_redirection.set_force_token_request(False)

    # Create the adapter and call the method
    adapter = HostedPaymentAdapter(setup_credentials)
    result = adapter.send_hosted_payment_request(hosted_payment_redirection)

    # Check the response
    response_url = result.get_redirect_url()
    assert response_url == "http://redirect.url"

    # Capture the network call arguments
    mock_send_request.assert_called_once()
    call_args = mock_send_request.call_args
    headers = call_args[1]['headers']
    query_parameters = call_args[1]['query_parameters']
    url = call_args[1]['url']
    print(query_parameters["integrityCheck"])
    # Verify the network call arguments
    assert headers["apiVersion"] == "5"
    assert headers["encryptionMode"] == "CBC"
    assert headers["iv"] == encoded_iv
    assert query_parameters["merchantId"] == "111222"
    assert query_parameters["encrypted"] == ("BKmgd7dcbBkUTMrv+aDMntkM7zsbqQbey64xnoNTtoRCtkNGJQL3PhyvlUgX+73e/"
                                             "+KrxopBFnjcmkbY/ChTw/LWJgL3zEc2rFE82c5mMkZ8w/e28qOcdMAmP62ZF+CoKl"
                                             "KsOWnDOsbswy7saDOaT1EMgjcF66bgeUJcdYhMtpJKyeD9+LPdyCNxPXqNc6l27epJ"
                                             "YQ/2+YeukYroPtxXSrra00fIwj2fJwzLeFa6j0Hi+r7Qdw9mZ++WPdeJd/IgpLG+j23"
                                             "pKJ1FYaK1iRf3DwVCW7dHfVb10NDnzh4Q2O5qzHsXzXZrPe8m5nLLKm2rNadRg4VC"
                                             "G/DVF+aDZPsFx4uq0B8X//JHzvsiS20JtCCwEDY6I+0NAJwbZ3FqBYBb55dUkQRGLz/"
                                             "vZGXcIsnENeA6dv7A/ZUHx4yE176mIyE5ejKCeaIOo+EizD3CAfcZX9Wnteg0ie/qkC"
                                             "hgfOdrN+AgyQd7yHpw7TTam1jpQ+85dgMoZTViydvfz4aJYZ5zy9jAY4ZG/1tU9MWX2"
                                             "PG7LQ==")
    assert query_parameters["integrityCheck"] == "7291075a33358698a895f8cc3700ea829e8ad4c8905115c00a3894f62e311030"
    assert url == Endpoints.HOSTED_ENDPOINT_STG.value  # Change this to the correct endpoint


def test_send_hosted_recurring_returns_redirect_url_on_success(setup_credentials, mocker):
    # Mock the network adapter send_request method
    mock_send_request = mocker.patch.object(NetworkAdapter, 'send_request', return_value=(200, "http://redirect.url"))

    # Create the HostedPaymentRedirection object
    request = HostedPaymentRecurrentInitial()
    request.set_amount("50")
    request.set_currency(Currency.EUR)
    request.set_country(CountryCodeAlpha2.ES)
    request.set_customer_id("903")
    request.set_merchant_transaction_id("3123123")
    request.set_payment_recurring_type(PaymentRecurringType.newCof)
    request.set_payment_solution(PaymentSolutions.creditcards)
    request.set_status_url(mock_configurations["statusUrl"])
    request.set_success_url(mock_configurations["baseURL"] + mock_configurations["successUrl"])
    request.set_error_url(mock_configurations["baseURL"] + mock_configurations["errorUrl"])
    request.set_awaiting_url(mock_configurations["baseURL"] + mock_configurations["awaitingUrl"])
    request.set_cancel_url(mock_configurations["baseURL"] + mock_configurations["cancelUrl"])
    request.set_force_token_request(False)
    print(request.get_merchant_transaction_id())
    # Create the adapter and call the method
    adapter = HostedPaymentAdapter(setup_credentials)
    result = adapter.send_hosted_payment_recurrent_initial(request)

    # Check the response
    response_url = result.get_redirect_url()
    assert response_url == "http://redirect.url"

    # Capture the network call arguments
    mock_send_request.assert_called_once()
    call_args = mock_send_request.call_args
    headers = call_args[1]['headers']
    query_parameters = call_args[1]['query_parameters']
    url = call_args[1]['url']
    print(query_parameters["integrityCheck"])
    # Verify the network call arguments
    assert headers["apiVersion"] == "5"
    assert headers["encryptionMode"] == "CBC"
    assert headers["iv"] == encoded_iv
    assert query_parameters["merchantId"] == "111222"
    assert query_parameters["encrypted"] == ("m//xJAl85GXjjlaL/ynPqdjNKz3CPql03EsA3jCTF9eHgHjSkSSteYWxnHxypstzDB2H"
                                             "TvSw2FcDlUBI0V4wF66Lb69ugIKy6ueGlrgv6Ugk7DGDbPkdYZL7xcJ5QUXtptP6pjQo"
                                             "t1r2gAJfnid3OnEqKVOQCsq9cOZeB44jNLH7/Z2MtAtgbBOMWYBbeZxXISH5Vdc7pV5ta"
                                             "La4Qi5PHqMwFXcVBmwrTyPH2cyfgDDre61H/NlYzEg0r9IA5/dAfnSwFzlSkamYb6A4PXw"
                                             "C64rtpQqFfnObcyNPxWDk2kjS2cjNSZChLDCr3p4U77DKtYBjTXbIgBcRcdsJLyremS7Vg"
                                             "1PHSopjkvrp5lrd8OVkj1gHMIKES5Oo4nwUOVoumnNzN7do6/Z0fGL6Ya8TNn4F6kBUre/"
                                             "SF7qLmq22ptQaHXX0LMNAdEn711iHya/a5JtW+RzF/EYNdaVyy5a9pg7l5x5CrviVlA6Bo"
                                             "dIYR5xAZ0PxcGEfVPqR5dvaFwgFMbyTWFuglNy9bba6pdPl7Tv5me54zWRkEDhGH55fype"
                                             "QJnn6DCIYxSDpvjbDZsJJ")

    assert query_parameters["integrityCheck"] == "d552610e87f76d7d8f0cc5084421082ae10f55a641f4ced3f56267f01a4c8413"
    assert url == Endpoints.HOSTED_ENDPOINT_STG.value  # Change this to the correct endpoint


@pytest.mark.parametrize("missing_field", [
    "currency",
    "amount",
    "country",
    "customerId",
    "merchantTransactionId",
    "paymentSolution",
    "statusURL",
    "successURL",
    "errorURL",
    "cancelURL",
    "awaitingURL",
])
def test_missing_mandatory_field_throws_exception(setup_credentials, missing_field):
    # Create the HostedPaymentRedirection object with all mandatory fields set
    hosted_payment_redirection = HostedPaymentRedirection()
    hosted_payment_redirection.set_amount("50")
    hosted_payment_redirection.set_currency(Currency.EUR)
    hosted_payment_redirection.set_country(CountryCodeAlpha2.ES)
    hosted_payment_redirection.set_customer_id("903")
    hosted_payment_redirection.set_merchant_transaction_id("3123123")
    hosted_payment_redirection.set_payment_solution(PaymentSolutions.creditcards)
    hosted_payment_redirection.set_status_url(mock_configurations["statusUrl"])
    hosted_payment_redirection.set_success_url(mock_configurations["baseURL"] + mock_configurations["successUrl"])
    hosted_payment_redirection.set_error_url(mock_configurations["baseURL"] + mock_configurations["errorUrl"])
    hosted_payment_redirection.set_awaiting_url(mock_configurations["baseURL"] + mock_configurations["awaitingUrl"])
    hosted_payment_redirection.set_cancel_url(mock_configurations["baseURL"] + mock_configurations["cancelUrl"])
    hosted_payment_redirection.set_force_token_request(False)

    # Remove the specified mandatory field
    setattr(hosted_payment_redirection, f"_HostedPaymentRedirection__{missing_field}", None)

    # Create the adapter
    adapter = HostedPaymentAdapter(setup_credentials)

    # Assert that MissingFieldException is raised with the expected message when the request is sent
    with pytest.raises(MissingFieldException) as exc_info:
        adapter.send_hosted_payment_request(hosted_payment_redirection)

    assert str(exc_info.value) == f"Missing {missing_field}"
