import os

import pytest

from sdk.adapters.h2h_payment_adapter import H2HPaymentAdapter
from sdk.adapters.network_adapter import NetworkAdapter
from sdk.enums.country_code import CountryCodeAlpha2
from sdk.enums.currency import Currency
from sdk.enums.endpoints import Endpoints
from sdk.enums.environment import Environment
from sdk.enums.payment_recurring_type import PaymentRecurringType
from sdk.enums.payment_solutions import PaymentSolutions
from sdk.exceptions.field_exception import MissingFieldException
from sdk.models.credentials import Credentials
from sdk.models.requests.h2h.h2h_payment_recurrent_initial import H2HPaymentRecurrentInitial
from sdk.models.requests.h2h.h2h_pre_authorization import H2HPreAuthorization
from sdk.models.requests.h2h.h2h_pre_authorization_capture import H2HPreAuthorizationCapture
from sdk.models.requests.h2h.h2h_redirection import H2HRedirection
from sdk.models.requests.h2h.h2h_refund import H2HRefund
from sdk.models.requests.h2h.h2h_void import H2HVoid
from sdk.utils.security_utils import SecurityUtils

# Mock configurations
mock_configurations = {
    "merchantId": "116819",
    "merchantPassword": "a193a2de8ed6140e848d5015620e8129",
    "productId": "1168190001",
    "statusUrl": "https://test.com/status",
    "successUrl": "https://test.com/success",
    "errorUrl": "https://test.com/fail",
    "awaitingUrl": "https://test.com/await",
    "cancelUrl": "https://test.com/cancel"
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


def read_xml_content(file_name):
    # Get the directory of the current file (test_notifications.py)
    current_file_directory = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the notifications directory relative to the current file
    xml_file_path = os.path.join(current_file_directory, 'notifications', file_name)

    if not os.path.exists(xml_file_path):
        raise FileNotFoundError(f"The file {xml_file_path} was not found.")

    with open(xml_file_path, 'r') as file:
        return file.read()


def test_send_h2h_returns_success_on_valid_request(setup_credentials, mocker):
    mock_send_request = mocker.patch.object(NetworkAdapter, 'send_request',
                                            return_value=(200, read_xml_content('h2h_response.xml')))

    # Create the H2HRedirection object
    h2h_redirection = H2HRedirection()
    h2h_redirection.set_amount("50.4321222")
    h2h_redirection.set_currency(Currency.EUR)
    h2h_redirection.set_country(CountryCodeAlpha2.ES)
    h2h_redirection.set_card_number("4907270002222227")
    h2h_redirection.set_customer_id("903")
    h2h_redirection.set_merchant_transaction_id("33312")
    h2h_redirection.set_ch_name("First name Last name")
    h2h_redirection.set_cvn_number("123")
    h2h_redirection.set_exp_date("0625")
    h2h_redirection.set_payment_solution(PaymentSolutions.creditcards)
    h2h_redirection.set_status_url(mock_configurations["statusUrl"])
    h2h_redirection.set_success_url(mock_configurations["successUrl"])
    h2h_redirection.set_error_url(mock_configurations["errorUrl"])
    h2h_redirection.set_awaiting_url(mock_configurations["awaitingUrl"])
    h2h_redirection.set_cancel_url(mock_configurations["cancelUrl"])

    # Create the adapter and call the method
    adapter = H2HPaymentAdapter(setup_credentials)
    result = adapter.send_h2h_payment_request(h2h_redirection)

    # Check the response
    redirect_url = result.get_notification().get_redirect_url()
    assert redirect_url == ('https://checkout.stg-eu-west3.epgint.com/EPGCheckout/rest/online/3dsv2/redirect?'
                            'action=gatherdevice&params=eyJ0aHJlZURTdjJUb2tlbiI6ImQ1NmEzNTVlLTQ4NjktNDFhNy1iOT'
                            'RiLTAxNWMwYzVkZTIwNiIsInRocmVlRFNNZXRob2RVcmwiOiJodHRwczovL21vY2stZHMuc3RnLWV1LXd'
                            'lc3QzLmVwZ2ludC5jb20vcHVibGljL21ldGhvZC1kYXRhLyIsInRocmVlRFNNZXRob2REYXRhIjoiZXlK'
                            'MGFISmxaVVJUVTJWeWRtVnlWSEpoYm5OSlJDSTZJbVExTm1Fek5UVmxMVFE0TmprdE5ERmhOeTFpT1RSaU'
                            'xUQXhOV013WXpWa1pUSXdOaUlzSUNKMGFISmxaVVJUVFdWMGFHOWtUbTkwYVdacFkyRjBhVzl1VlZKTUlq'
                            'b2dJbWgwZEhCek9pOHZZMmhsWTJ0dmRYUXVjM1JuTFdWMUxYZGxjM1F6TG1Wd1oybHVkQzVqYjIwdlJWQk'
                            'hRMmhsWTJ0dmRYUXZZMkZzYkdKaFkyc3ZaMkYwYUdWeVJHVjJhV05sVG05MGFXWnBZMkYwYVc5dUwzQmhl'
                            'WE52YkM4elpITjJNaTh4TURJeE5qTTJJbjA9IiwiYnJhbmQiOm51bGwsInJlc3VtZUF1dGhlbnRpY2F0aW'
                            '9uIjoiaHR0cHM6Ly9jaGVja291dC5zdGctZXUtd2VzdDMuZXBnaW50LmNvbS9FUEdDaGVja291dC9yZXR1'
                            'cm51cmwvZnJpY3Rpb25sZXNzL3BheXNvbC8zZHN2Mi8xMDIxNjM2P3RocmVlRFN2MlRva2VuPWQ1NmEzNT'
                            'VlLTQ4NjktNDFhNy1iOTRiLTAxNWMwYzVkZTIwNiIsInJlbmRlckNhc2hpZXJMb2NhdGlvbiI6Imh0dHBz'
                            'Oi8vZXBnanMtcmVuZGVyY2FzaGllci1zdGcuZWFzeXBheW1lbnRnYXRld2F5LmNvbSIsImNoYWxsZW5nZVd'
                            'pbmRvd3NTaXplIjoiMDUifQ==')

    # Capture the network call arguments
    mock_send_request.assert_called_once()
    call_args = mock_send_request.call_args
    headers = call_args[1]['headers']
    query_parameters = call_args[1]['query_parameters']
    url = call_args[1]['url']

    # Verify the network call arguments
    assert headers["apiVersion"] == "5"
    assert headers["encryptionMode"] == "CBC"
    assert headers["iv"] == encoded_iv
    assert query_parameters["merchantId"] == "116819"
    assert query_parameters[
               "encrypted"] == ("rYtHWBRT/f3TfGQ0dgZaGxAIfMoZqbiUD3XSaz1XO+GalC6Z9tYVDp8pP9ueY4nW1LoYB5RuNdKP48s7R"
                                "+A6jlL7pFpfLXPfyYbhrauYcKH70MQTaNOtokhU1T6ZYTxSXGeCJssYPu6/G1p87kwIDp8VBirL9Z"
                                "URJDPVInkFOb1IXHm281KDGzlbyH7Uru7wPP4nG7PaKM22cqayRbgPoyG1DcEP7DXOGBvZB7NYNCPT"
                                "MbxUYE+ev/J5jaAAfdJfFhSQ1SeTTUMWSO420WUk//b3XxZmMs6UF+SpOk/bZgrxvkHBKQ2UQecHXvbs"
                                "2kh+jliZhmcZX6WZT/ZrevWq7vldIalMbWDFCntgnqtBlTyrjht35BPbByCMVnjkCaG8CoKdfJUTyUBSs"
                                "bqY0aQXWTB/WHRzMI1nOxgW0192iUyrw04+mioZYStxfSIJYvDm4W63/f3TKf10P2BwktFQxR8iSmYihYDlU"
                                "q6A5BUDYha/bbYl1xoty3/xVDqY+lNxFiV9cE1u9RFgoJi/e/DO+P3/6LjQfTUdabwsLL5gKMlkBwug5Qhxj"
                                "tCV+wzRQLMmAcHQw4FuDeEza9s8WKHuF/H2AxQk0K99VLqurxphe0DrUF7yDpT44BgL018W+XnL")

    # Replace static value with the actual expected value
    assert query_parameters["integrityCheck"] == "8dee75c53942050c5c368b7262601c0f0db6c13688fdb9e97076c5a38afe9218"
    assert url == Endpoints.H2H_ENDPOINT_STG.value  # Change this to the correct endpoint


@pytest.mark.parametrize("missing_field", [
    "amount",
    "country",
    "currency",
    "customerId",
    "merchantTransactionId",
    "paymentSolution",
    "statusURL",
    "successURL",
    "errorURL",
    "cancelURL",
    "awaitingURL",
    "chName",
    "cardNumber",
    "expDate",
    "cvnNumber"
])
def test_missing_mandatory_field_throws_exception_h2h(setup_credentials, missing_field):
    # Create the H2HRedirection object with all mandatory fields set
    h2h_redirection = H2HRedirection()
    h2h_redirection.set_amount("50.4321222")
    h2h_redirection.set_currency(Currency.EUR)
    h2h_redirection.set_country(CountryCodeAlpha2.ES)
    h2h_redirection.set_card_number("4907270002222227")
    h2h_redirection.set_customer_id("903")
    h2h_redirection.set_merchant_transaction_id("33312")
    h2h_redirection.set_ch_name("First name Last name")
    h2h_redirection.set_cvn_number("123")
    h2h_redirection.set_exp_date("0625")
    h2h_redirection.set_payment_solution(PaymentSolutions.creditcards)
    h2h_redirection.set_status_url(mock_configurations["statusUrl"])
    h2h_redirection.set_success_url(mock_configurations["successUrl"])
    h2h_redirection.set_error_url(mock_configurations["errorUrl"])
    h2h_redirection.set_awaiting_url(mock_configurations["awaitingUrl"])
    h2h_redirection.set_cancel_url(mock_configurations["cancelUrl"])

    # Remove the specified mandatory field
    setattr(h2h_redirection, f"_H2HRedirection__{missing_field}", None)

    # Create the adapter
    adapter = H2HPaymentAdapter(setup_credentials)

    # Assert that MissingFieldException is raised with the expected message when the request is sent
    with pytest.raises(MissingFieldException) as exc_info:
        adapter.send_h2h_payment_request(h2h_redirection)

    assert str(exc_info.value) == f"Missing {missing_field}"


def test_send_h2h_capture_success_on_valid_request(setup_credentials, mocker):
    # Mock the network adapter send_request method
    mock_send_request = mocker.patch.object(NetworkAdapter, 'send_request',
                                            return_value=(200, read_xml_content('h2h_capture.xml')))

    # Create the H2HRedirection object
    request = H2HPreAuthorizationCapture()
    request.set_payment_solution(PaymentSolutions.caixapucpuce)
    request.set_transaction_id("7961829")
    request.set_merchant_transaction_id("344122331")

    # Create the adapter and call the method
    adapter = H2HPaymentAdapter(setup_credentials)
    result = adapter.send_h2h_pre_authorization_capture(request)

    # Check the response
    status = result.get_notification().operations[-1].status
    assert status == 'SUCCESS'

    # Capture the network call arguments
    mock_send_request.assert_called_once()
    call_args = mock_send_request.call_args
    headers = call_args[1]['headers']
    query_parameters = call_args[1]['query_parameters']
    url = call_args[1]['url']

    # Verify the network call arguments
    assert headers["apiVersion"] == "5"
    assert headers["encryptionMode"] == "CBC"
    assert headers["iv"] == encoded_iv
    assert query_parameters["merchantId"] == "116819"
    assert query_parameters["encrypted"] == ("bM+53umBrdJi5cCM5U1SrKRKcntj/9xSZgCycrdAXAEVywiMk10go+oFP8fwd/0zgZl/7/"
                                             "FkqoHRx4Meve+qOyhfEde43LrhsGug+n7ueD2Jxbw7VFMZtDhodhQ67Nerqc8KJ"
                                             "2WZaRRD6+7pUR4KBw==")

    # Replace static with the actual expected value
    assert query_parameters["integrityCheck"] == "5386f5a1ce8a3e870169b7dc45074193ba7da8c38cad8e02f6d24c38ad850b4c"
    assert url == Endpoints.CAPTURE_ENDPOINT_STG.value  # Change this to the correct endpoint


@pytest.mark.parametrize("missing_field", [
    "paymentSolution",
    "transactionId",
    "merchantTransactionId",
])
def test_missing_mandatory_field_throws_exception_h2h_capture(setup_credentials, missing_field):
    # Create the H2HPreAuthorizationCapture object with all mandatory fields set
    request = H2HPreAuthorizationCapture()
    request.set_payment_solution(PaymentSolutions.caixapucpuce)
    request.set_transaction_id("7961829")
    request.set_merchant_transaction_id("344122331")

    # Remove the specified mandatory field
    setattr(request, f"_H2HPreAuthorizationCapture__{missing_field}", None)

    # Create the adapter
    adapter = H2HPaymentAdapter(setup_credentials)

    # Assert that MissingFieldException is raised with the expected message when the request is sent
    with pytest.raises(MissingFieldException) as exc_info:
        adapter.send_h2h_pre_authorization_capture(request)

    assert str(exc_info.value) == f"Missing {missing_field}"


def test_send_h2h_void_success_on_valid_request(setup_credentials, mocker):
    # Mock the network adapter send_request method
    mock_send_request = mocker.patch.object(NetworkAdapter, 'send_request',
                                            return_value=(200, read_xml_content('h2h_void.xml')))

    # Create the H2HRedirection object
    request = H2HVoid()
    request.set_payment_solution(PaymentSolutions.caixapucpuce)
    request.set_transaction_id("7817740")
    request.set_merchant_transaction_id("76969499")

    # Create the adapter and call the method
    adapter = H2HPaymentAdapter(setup_credentials)
    result = adapter.send_h2h_void_request(request)

    # Check the response
    status = result.get_notification().operations[-1].status
    assert status == 'SUCCESS'

    # Capture the network call arguments
    mock_send_request.assert_called_once()
    call_args = mock_send_request.call_args
    headers = call_args[1]['headers']
    query_parameters = call_args[1]['query_parameters']
    url = call_args[1]['url']

    # Verify the network call arguments
    assert headers["apiVersion"] == "5"
    assert headers["encryptionMode"] == "CBC"
    assert headers["iv"] == encoded_iv
    assert query_parameters["merchantId"] == "116819"
    assert query_parameters["encrypted"] == ("bM+53umBrdJi5cCM5U1SrKRKcntj/9xSZgCycrdAXAHLi+DLsLRxkQ+u1w1BDrld/"
                                             "8Ukvd1EOOrg9YtnPfW8fQmZbb3nbcm8FmLSVKi23EgyJkhuGA720ArPiSiEhWS7Xy"
                                             "JS3VFcyXuwxO3AEORRsw==")

    # Replace static with the actual expected value
    assert query_parameters["integrityCheck"] == "ecef828a3b5c06f3f3b12ba84458465b10bff296b95e2730bdcb43aecab97147"
    assert url == Endpoints.VOID_ENDPOINT_STG.value  # Change this to the correct endpoint


@pytest.mark.parametrize("missing_field", [
    "paymentSolution",
    "transactionId",
    "merchantTransactionId",
])
def test_missing_mandatory_field_throws_exception_h2h_void(setup_credentials, missing_field):
    # Create the H2HVoid object with all mandatory fields set
    request = H2HVoid()
    request.set_payment_solution(PaymentSolutions.caixapucpuce)
    request.set_transaction_id("7817740")
    request.set_merchant_transaction_id("76969499")

    # Remove the specified mandatory field
    setattr(request, f"_H2HVoid__{missing_field}", None)

    # Create the adapter
    adapter = H2HPaymentAdapter(setup_credentials)

    # Assert that MissingFieldException is raised with the expected message when the request is sent
    with pytest.raises(MissingFieldException) as exc_info:
        adapter.send_h2h_void_request(request)

    assert str(exc_info.value) == f"Missing {missing_field}"


def test_send_h2h_refund_success_on_valid_request(setup_credentials, mocker):
    # Mock the network adapter send_request method
    mock_send_request = mocker.patch.object(NetworkAdapter, 'send_request',
                                            return_value=(200, read_xml_content('h2h_refund.xml')))

    # Create the H2HRedirection object
    request = H2HRefund()
    request.set_amount("20")
    request.set_payment_solution(PaymentSolutions.caixapucpuce)
    request.set_merchant_transaction_id("38559715")
    request.set_transaction_id("7817556")

    # Create the adapter and call the method
    adapter = H2HPaymentAdapter(setup_credentials)
    result = adapter.send_h2h_refund_request(request)

    # Check the response
    status = result.get_notification().operations[-1].status
    assert status == 'SUCCESS'

    # Capture the network call arguments
    mock_send_request.assert_called_once()
    call_args = mock_send_request.call_args
    headers = call_args[1]['headers']
    query_parameters = call_args[1]['query_parameters']
    url = call_args[1]['url']

    # Verify the network call arguments
    assert headers["apiVersion"] == "5"
    assert headers["encryptionMode"] == "CBC"
    assert headers["iv"] == encoded_iv
    assert query_parameters["merchantId"] == "116819"
    assert query_parameters["encrypted"] == ("KLPDp/+WmWX4JyZVXiND3BkJ+1ZjLvhvfDXDoWflB7Udn0Wc/"
                                             "JI9nPwntB+5xdFNCX8UTE5NefWe4FvtKRlw7lIv6RSuHTHd8CVohzcLL"
                                             "GouPp6yCfdBOMjbVbc5iClTc7r1PXYZ0A8+BigSLAQu+GyddrSsrPqoFwzfINzGs/o=")

    # Replace static with the actual expected value
    assert query_parameters["integrityCheck"] == "1061275cf0ca1e3d58f072a56746dafbfd27d5456fbdf1efe47115e1cd8fd14d"
    assert url == Endpoints.REFUND_ENDPOINT_STG.value  # Change this to the correct endpoint


@pytest.mark.parametrize("missing_field", [
    "amount",
    "paymentSolution",
    "merchantTransactionId",
    "transactionId",
])
def test_missing_mandatory_field_throws_exception_h2h_refund(setup_credentials, missing_field):
    # Create the H2HRefund object with all mandatory fields set
    request = H2HRefund()
    request.set_amount("20")
    request.set_payment_solution(PaymentSolutions.caixapucpuce)
    request.set_merchant_transaction_id("38559715")
    request.set_transaction_id("7817556")

    # Remove the specified mandatory field
    setattr(request, f"_H2HRefund__{missing_field}", None)

    # Create the adapter
    adapter = H2HPaymentAdapter(setup_credentials)

    # Assert that MissingFieldException is raised with the expected message when the request is sent
    with pytest.raises(MissingFieldException) as exc_info:
        adapter.send_h2h_refund_request(request)

    assert str(exc_info.value) == f"Missing {missing_field}"


def test_send_h2h_pre_authorization_returns_success_on_valid_request(setup_credentials, mocker):
    # Mock the network adapter send_request method
    mock_send_request = mocker.patch.object(NetworkAdapter, 'send_request',
                                            return_value=(200, read_xml_content('h2h_preauthorization.xml')))

    # Create the H2HRedirection object
    request = H2HPreAuthorization()
    request.set_amount("50")
    request.set_currency(Currency.EUR)
    request.set_country(CountryCodeAlpha2.ES)
    request.set_merchant_transaction_id("3311223")
    request.set_card_number("4907270002222227")
    request.set_customer_id("903")
    request.set_ch_name("First name Last name")
    request.set_cvn_number("123")
    request.set_exp_date("0625")
    request.set_auto_capture(False)
    request.set_payment_solution(PaymentSolutions.creditcards)
    request.set_status_url(mock_configurations["statusUrl"])
    request.set_success_url(mock_configurations["successUrl"])
    request.set_error_url(mock_configurations["errorUrl"])
    request.set_awaiting_url(mock_configurations["awaitingUrl"])
    request.set_cancel_url(mock_configurations["cancelUrl"])

    # Create the adapter and call the method
    adapter = H2HPaymentAdapter(setup_credentials)
    result = adapter.send_h2h_pre_authorization_request(request)

    # Check the response
    redirect_url = result.get_notification().get_redirect_url()
    assert redirect_url == ('https://checkout.stg-eu-west3.epgint.com/EPGCheckout/rest/online/3dsv2/'
                            'redirect?action=gatherdevice&params=eyJ0aHJlZURTdjJUb2tlbiI6IjM2ODU5NGM2LTUzM'
                            'DItNDlhOC04NThhLTFkNTgwOTM3N2Q0YSIsInRocmVlRFNNZXRob2RVcmwiOiJodHRwczovL21vY2s'
                            'tZHMuc3RnLWV1LXdlc3QzLmVwZ2ludC5jb20vcHVibGljL21ldGhvZC1kYXRhLyIsInRocmVlRFNNZ'
                            'XRob2REYXRhIjoiZXlKMGFISmxaVVJUVTJWeWRtVnlWSEpoYm5OSlJDSTZJak0yT0RVNU5HTTJMVFV6T'
                            'URJdE5EbGhPQzA0TlRoaExURmtOVGd3T1RNM04yUTBZU0lzSUNKMGFISmxaVVJUVFdWMGFHOWtUbTkwYV'
                            'dacFkyRjBhVzl1VlZKTUlqb2dJbWgwZEhCek9pOHZZMmhsWTJ0dmRYUXVjM1JuTFdWMUxYZGxjM1F6TG1'
                            'Wd1oybHVkQzVqYjIwdlJWQkhRMmhsWTJ0dmRYUXZZMkZzYkdKaFkyc3ZaMkYwYUdWeVJHVjJhV05sVG05M'
                            'GFXWnBZMkYwYVc5dUwzQmhlWE52YkM4elpITjJNaTh4TURJeE9EZzRJbjA9IiwiYnJhbmQiOm51bGwsInJ'
                            'lc3VtZUF1dGhlbnRpY2F0aW9uIjoiaHR0cHM6Ly9jaGVja291dC5zdGctZXUtd2VzdDMuZXBnaW50LmNvbS9F'
                            'UEdDaGVja291dC9yZXR1cm51cmwvZnJpY3Rpb25sZXNzL3BheXNvbC8zZHN2Mi8xMDIxODg4P3RocmVlRFN2M'
                            'lRva2VuPTM2ODU5NGM2LTUzMDItNDlhOC04NThhLTFkNTgwOTM3N2Q0YSIsInJlbmRlckNhc2hpZXJMb2NhdG'
                            'lvbiI6Imh0dHBzOi8vZXBnanMtcmVuZGVyY2FzaGllci1zdGcuZWFzeXBheW1lbnRnYXRld2F5LmNvbSIsIm'
                            'NoYWxsZW5nZVdpbmRvd3NTaXplIjoiMDUifQ==')

    # Capture the network call arguments
    mock_send_request.assert_called_once()
    call_args = mock_send_request.call_args
    headers = call_args[1]['headers']
    query_parameters = call_args[1]['query_parameters']
    url = call_args[1]['url']

    # Verify the network call arguments
    assert headers["apiVersion"] == "5"
    assert headers["encryptionMode"] == "CBC"
    assert headers["iv"] == encoded_iv
    assert query_parameters["merchantId"] == "116819"
    assert query_parameters["encrypted"] == ("rYtHWBRT/f3TfGQ0dgZaG59KNlFg/TNM38A2kD3jutNB0+mMXN2ynE9oo50i28SkyzR42i"
                                             "ONfPW/i2vb2SjixkxJtf1OIH43Vue39H0HGFa32luMRTQyKD8T8o/PD5okoD3zXOTmXbsn"
                                             "hCP8xWAHYYbG9Qx/Uyg0Brc9pwJpMvaDHsSgFBJnE9Q6pUW43y2EetWLHWqoxODPdgXfjeZ"
                                             "tPWNxwkuJq1pbROUyJr3P5TrQDEj6HlJdaGDDpU5VZHhAb6FFe1zJQmUfAZdbEGKtStlv5L"
                                             "l/0aJE7wNaAd3Ps19nCtfoxIltlpBXodx58AxC6JbxFpJ8FYQMb60jrhqCyfLN3ElXZxoLq"
                                             "WgsRAwxXPBuYwC8mUoX/en8GjqozKCSBgTMx1Z7VNM1pwHt/6dLNU1ZYE4oAqLPGKXHpZ2e"
                                             "8ynXwXm+A4138eFWzHf/mQSKBQYzDI/Hx+pEmBxvapsA3LqNd7TkiYVfTZW9OWqMLnLLCSB"
                                             "YAS2XzIrZQrwZbOCRQWlvs9qeLRJo4M3+imz5qPvzGadk2jHG3g6sPoksk/ZnOWd807oTXa6"
                                             "P3VgHQ1DfedFUsH/fGeSs66BdhSdPjuUTxs1Mpm5K2sZtDkwWvudM6Rh6Ea8ZUNTTb1ZaDgz"
                                             "T0d2IX5bUDVOap7aiUCxrfQ==")

    # Replace static value with the actual expected value
    assert query_parameters["integrityCheck"] == "74be677c67433218188665cbc865e69888eb3ea16632c1935d8ed353fbcadf5e"
    assert url == Endpoints.H2H_ENDPOINT_STG.value  # Change this to the correct endpoint


@pytest.mark.parametrize("missing_field", [
    "amount",
    "country",
    "currency",
    "customerId",
    "merchantTransactionId",
    "paymentSolution",
    "statusURL",
    "successURL",
    "errorURL",
    "cancelURL",
    "awaitingURL",
    "chName",
    "autoCapture",
    "cardNumber",
    "expDate",
    "cvnNumber"
])
def test_missing_mandatory_field_throws_exception_h2h_pre_authorization(setup_credentials, missing_field):
    # Create the H2HPreAuthorization object with all mandatory fields set
    request = H2HPreAuthorization()
    request.set_amount("50")
    request.set_currency(Currency.EUR)
    request.set_country(CountryCodeAlpha2.ES)
    request.set_merchant_transaction_id("3311223")
    request.set_card_number("4907270002222227")
    request.set_customer_id("903")
    request.set_ch_name("First name Last name")
    request.set_cvn_number("123")
    request.set_exp_date("0625")
    request.set_auto_capture(False)
    request.set_payment_solution(PaymentSolutions.creditcards)
    request.set_status_url(mock_configurations["statusUrl"])
    request.set_success_url(mock_configurations["successUrl"])
    request.set_error_url(mock_configurations["errorUrl"])
    request.set_awaiting_url(mock_configurations["awaitingUrl"])
    request.set_cancel_url(mock_configurations["cancelUrl"])

    # Remove the specified mandatory field
    setattr(request, f"_H2HRedirection__{missing_field}", None)
    setattr(request, f"_H2HPreAuthorization__{missing_field}", None)

    # Create the adapter
    adapter = H2HPaymentAdapter(setup_credentials)

    # Assert that MissingFieldException is raised with the expected message when the request is sent
    with pytest.raises(Exception) as exc_info:
        adapter.send_h2h_pre_authorization_request(request)

    assert str(exc_info.value) == f"Missing {missing_field}"


def test_send_h2h_recurring_returns_success_on_valid_request(setup_credentials, mocker):
    # Mock the network adapter send_request method
    mock_send_request = mocker.patch.object(NetworkAdapter, 'send_request',
                                            return_value=(200, read_xml_content('h2h_recurring.xml')))

    # Create the H2HPaymentRecurrentInitial object
    request = H2HPaymentRecurrentInitial()
    request.set_amount("50")
    request.set_currency(Currency.EUR)
    request.set_country(CountryCodeAlpha2.ES)
    request.set_merchant_transaction_id("3331231")
    request.set_payment_solution(PaymentSolutions.creditcards)
    request.set_card_number("4907270002222227")
    request.set_customer_id("55")
    request.set_ch_name("First name Last name")
    request.set_cvn_number("123")
    request.set_exp_date("0625")
    request.set_status_url(mock_configurations["statusUrl"])
    request.set_success_url(mock_configurations["successUrl"])
    request.set_error_url(mock_configurations["errorUrl"])
    request.set_awaiting_url(mock_configurations["awaitingUrl"])
    request.set_cancel_url(mock_configurations["cancelUrl"])
    request.set_payment_recurring_type(PaymentRecurringType.newCof)

    # Create the adapter and call the method
    adapter = H2HPaymentAdapter(setup_credentials)
    result = adapter.send_h2h_payment_recurrent_initial(request)

    # Check the response
    redirect_url = result.get_notification().get_redirect_url()
    assert redirect_url == ('https://checkout.stg-eu-west3.epgint.com/EPGCheckout/rest/online/3dsv2/redirect?'
                            'action=gatherdevice&params=eyJ0aHJlZURTdjJUb2tlbiI6IjM2ODU5NGM2LTUzMDItNDlhOC04NTh'
                            'hLTFkNTgwOTM3N2Q0YSIsInRocmVlRFNNZXRob2RVcmwiOiJodHRwczovL21vY2stZHMuc3RnLWV1LXdlc'
                            '3QzLmVwZ2ludC5jb20vcHVibGljL21ldGhvZC1kYXRhLyIsInRocmVlRFNNZXRob2REYXRhIjoiZXlKMGFI'
                            'SmxaVVJUVTJWeWRtVnlWSEpoYm5OSlJDSTZJak0yT0RVNU5HTTJMVFV6TURJdE5EbGhPQzA0TlRoaExURmtOV'
                            'Gd3T1RNM04yUTBZU0lzSUNKMGFISmxaVVJUVFdWMGFHOWtUbTkwYVdacFkyRjBhVzl1VlZKTUlqb2dJbWgwZE'
                            'hCek9pOHZZMmhsWTJ0dmRYUXVjM1JuTFdWMUxYZGxjM1F6TG1Wd1oybHVkQzVqYjIwdlJWQkhRMmhsWTJ0dmRY'
                            'UXZZMkZzYkdKaFkyc3ZaMkYwYUdWeVJHVjJhV05sVG05MGFXWnBZMkYwYVc5dUwzQmhlWE52YkM4elpITjJNaT'
                            'h4TURJeE9EZzRJbjA9IiwiYnJhbmQiOm51bGwsInJlc3VtZUF1dGhlbnRpY2F0aW9uIjoiaHR0cHM6Ly9jaGVj'
                            'a291dC5zdGctZXUtd2VzdDMuZXBnaW50LmNvbS9FUEdDaGVja291dC9yZXR1cm51cmwvZnJpY3Rpb25sZXNzL3'
                            'BheXNvbC8zZHN2Mi8xMDIxODg4P3RocmVlRFN2MlRva2VuPTM2ODU5NGM2LTUzMDItNDlhOC04NThhLTFkNTgwO'
                            'TM3N2Q0YSIsInJlbmRlckNhc2hpZXJMb2NhdGlvbiI6Imh0dHBzOi8vZXBnanMtcmVuZGVyY2FzaGllci1zdGcu'
                            'ZWFzeXBheW1lbnRnYXRld2F5LmNvbSIsImNoYWxsZW5nZVdpbmRvd3NTaXplIjoiMDUifQ==')

    # Capture the network call arguments
    mock_send_request.assert_called_once()
    call_args = mock_send_request.call_args
    headers = call_args[1]['headers']
    query_parameters = call_args[1]['query_parameters']
    url = call_args[1]['url']

    # Verify the network call arguments
    assert headers["apiVersion"] == "5"
    assert headers["encryptionMode"] == "CBC"
    assert headers["iv"] == encoded_iv
    assert query_parameters["merchantId"] == "116819"
    assert query_parameters["encrypted"] == ("9OBG4fXlgohwJDnyLqXOZE4XeuWsUOlJknClfaVOBMNSe03DqDDr+jdebshgr5CMf3X+"
                                             "sWkHGI6OnZsdeUg+t8LnS154W0NiNuc5UQGnUJhVL/efE0cdK1gQOSybsDj4S0LvnBnenfs"
                                             "/HVAwr/uFATFJVR9Mli5tybZdBqZ7rD0pBKFVLKt6KohS0HnioPQ3mg/oDC/xw1oU9l0xHs"
                                             "I2l95DSaXsbbPdnFfr9+3lUwICNUdlY/5PSt6tPcE8dn8TkoctfclCyNJau9FP5VzeAmKZL"
                                             "il+o/10xJI96z4k5WD0+5jRMXNNI+sYWa0tLc521mM07QqmZHV28wSDwKFhmDXgtzOeLPl8g"
                                             "ggII3nj4xGhyYXW76T6gUh9jhCy2TGkl6saOyJ74LUmfQwpaVeAwkqII5jKaLH96P7Hek"
                                             "C34sz3bUr0K0Av9k65ChYWcrwJk7B+sKSyAjg5COMa2FOrMwxHgdtrnnvlTX4eljNk3VZmE"
                                             "/VKQ8cbe9HCytmZ4LDXsXgZqJ3XgVGMHc26f2ingt/RlUjoyg1EOSOXnhZcDu/"
                                             "BE06G+L5FSJeIb8j2//IVq20IqDrTCtgohv3R0WzIPE3S60kFn66H+iTCCgsEwbKUJeYNl"
                                             "mmj40Ca5uYjlg6bm3Nq2laMV3kIXxLWE1v3BhxA80+ten4pDp0gqkSHt6M=")

    # Replace static value with the actual expected value
    assert query_parameters["integrityCheck"] == "a3004d83b25e6f7a2a15509de8f10ae0f9b15801af4c12dcad57d99dab7893b0"
    assert url == Endpoints.H2H_ENDPOINT_STG.value  # Change this to the correct endpoint


@pytest.mark.parametrize("missing_field", [
    "amount",
    "currency",
    "country",
    "merchantTransactionId",
    "paymentSolution",
    "cardNumber",
    "customerId",
    "chName",
    "cvnNumber",
    "expDate",
    "statusURL",
    "successURL",
    "errorURL",
    "awaitingURL",
    "cancelURL",
])
def test_missing_mandatory_field_throws_exception_h2h_recurring(setup_credentials, missing_field):
    # Create the H2HPaymentRecurrentInitial object with all mandatory fields set
    request = H2HPaymentRecurrentInitial()
    request.set_amount("50")
    request.set_currency(Currency.EUR)
    request.set_country(CountryCodeAlpha2.ES)
    request.set_merchant_transaction_id("3331231")
    request.set_payment_solution(PaymentSolutions.creditcards)
    request.set_card_number("4907270002222227")
    request.set_customer_id("55")
    request.set_ch_name("First name Last name")
    request.set_cvn_number("123")
    request.set_exp_date("0625")
    request.set_status_url(mock_configurations["statusUrl"])
    request.set_success_url(mock_configurations["successUrl"])
    request.set_error_url(mock_configurations["errorUrl"])
    request.set_awaiting_url(mock_configurations["awaitingUrl"])
    request.set_cancel_url(mock_configurations["cancelUrl"])
    request.set_payment_recurring_type(PaymentRecurringType.newCof)

    # Remove the specified mandatory field by setting it to None in the internal dictionary
    setattr(request, f"_H2HRedirection__{missing_field}", None)

    # Create the adapter
    adapter = H2HPaymentAdapter(setup_credentials)

    # Assert that MissingFieldException is raised with the expected message when the request is sent
    with pytest.raises(MissingFieldException) as exc_info:
        adapter.send_h2h_payment_recurrent_initial(request)

    assert str(exc_info.value) == f"Missing {missing_field}"


def test_send_h2h_recurring_subsuqent_returns_success_on_valid_request(setup_credentials, mocker):
    # Mock the network adapter send_request method
    mock_send_request = mocker.patch.object(NetworkAdapter, 'send_request',
                                            return_value=(200, read_xml_content('h2h_recurring_subsuqent.xml')))

    # Create the H2HPaymentRecurrentInitial object
    request = H2HPaymentRecurrentInitial()
    request.set_amount("50")
    request.set_currency(Currency.EUR)
    request.set_country(CountryCodeAlpha2.ES)
    request.set_merchant_transaction_id("3331231")
    request.set_payment_solution(PaymentSolutions.creditcards)
    request.set_card_number("4907270002222227")
    request.set_customer_id("55")
    request.set_ch_name("First name Last name")
    request.set_cvn_number("123")
    request.set_exp_date("0625")
    request.set_status_url(mock_configurations["statusUrl"])
    request.set_success_url(mock_configurations["successUrl"])
    request.set_error_url(mock_configurations["errorUrl"])
    request.set_awaiting_url(mock_configurations["awaitingUrl"])
    request.set_cancel_url(mock_configurations["cancelUrl"])
    request.set_payment_recurring_type(PaymentRecurringType.newCof)

    # Create the adapter and call the method
    adapter = H2HPaymentAdapter(setup_credentials)
    result = adapter.send_h2h_payment_recurrent_initial(request)

    # Check the response
    status = result.get_notification().operations[-1].status
    assert status == 'SUCCESS'

    # Capture the network call arguments
    mock_send_request.assert_called_once()
    call_args = mock_send_request.call_args
    headers = call_args[1]['headers']
    query_parameters = call_args[1]['query_parameters']
    url = call_args[1]['url']

    # Verify the network call arguments
    assert headers["apiVersion"] == "5"
    assert headers["encryptionMode"] == "CBC"
    assert headers["iv"] == encoded_iv
    assert query_parameters["merchantId"] == "116819"
    assert query_parameters["encrypted"] == ("9OBG4fXlgohwJDnyLqXOZE4XeuWsUOlJknClfaVOBMNSe03DqDDr+jdebshgr5CMf3X+"
                                             "sWkHGI6OnZsdeUg+t8LnS154W0NiNuc5UQGnUJhVL/efE0cdK1gQOSybsDj4S0LvnBn"
                                             "enfs/HVAwr/uFATFJVR9Mli5tybZdBqZ7rD0pBKFVLKt6KohS0HnioPQ3mg/oDC/xw1o"
                                             "U9l0xHsI2l95DSaXsbbPdnFfr9+3lUwICNUdlY/5PSt6tPcE8dn8TkoctfclCyNJau9FP5"
                                             "VzeAmKZLil+o/10xJI96z4k5WD0+5jRMXNNI+sYWa0tLc521mM07QqmZHV28wSDwKFhmD"
                                             "XgtzOeLPl8gggII3nj4xGhyYXW76T6gUh9jhCy2TGkl6saOyJ74LUmfQwpaVeAwkqII5jK"
                                             "aLH96P7HekC34sz3bUr0K0Av9k65ChYWcrwJk7B+sKSyAjg5COMa2FOrMwxHgdtrnnvlTX"
                                             "4eljNk3VZmE/VKQ8cbe9HCytmZ4LDXsXgZqJ3XgVGMHc26f2ingt/RlUjoyg1EOSOXnhZc"
                                             "Du/BE06G+L5FSJeIb8j2//IVq20IqDrTCtgohv3R0WzIPE3S60kFn66H+iTCCgsEwbKUJeY"
                                             "Nlmmj40Ca5uYjlg6bm3Nq2laMV3kIXxLWE1v3BhxA80+ten4pDp0gqkSHt6M=")

    # Replace static value with the actual expected value
    assert query_parameters["integrityCheck"] == "a3004d83b25e6f7a2a15509de8f10ae0f9b15801af4c12dcad57d99dab7893b0"
    assert url == Endpoints.H2H_ENDPOINT_STG.value  # Change this to the correct endpoint


@pytest.mark.parametrize("missing_field", [
    "amount",
    "currency",
    "country",
    "merchantTransactionId",
    "paymentSolution",
    "cardNumber",
    "customerId",
    "chName",
    "cvnNumber",
    "expDate",
    "statusURL",
    "successURL",
    "errorURL",
    "awaitingURL",
    "cancelURL",
])
def test_missing_mandatory_field_throws_exception_h2h_recurring_subsequent(setup_credentials, missing_field):
    # Create the H2HPaymentRecurrentInitial object with all mandatory fields set
    request = H2HPaymentRecurrentInitial()
    request.set_amount("50")
    request.set_currency(Currency.EUR)
    request.set_country(CountryCodeAlpha2.ES)
    request.set_merchant_transaction_id("3331231")
    request.set_payment_solution(PaymentSolutions.creditcards)
    request.set_card_number("4907270002222227")
    request.set_customer_id("55")
    request.set_ch_name("First name Last name")
    request.set_cvn_number("123")
    request.set_exp_date("0625")
    request.set_status_url(mock_configurations["statusUrl"])
    request.set_success_url(mock_configurations["successUrl"])
    request.set_error_url(mock_configurations["errorUrl"])
    request.set_awaiting_url(mock_configurations["awaitingUrl"])
    request.set_cancel_url(mock_configurations["cancelUrl"])
    request.set_payment_recurring_type(PaymentRecurringType.newCof)

    # Remove the specified mandatory field by setting it to None in the internal dictionary
    setattr(request, f"_H2HRedirection__{missing_field}", None)

    # Create the adapter
    adapter = H2HPaymentAdapter(setup_credentials)

    # Assert that MissingFieldException is raised with the expected message when the request is sent
    with pytest.raises(MissingFieldException) as exc_info:
        adapter.send_h2h_payment_recurrent_initial(request)

    assert str(exc_info.value) == f"Missing {missing_field}"
