import os
from decimal import Decimal
from typing import List

import pytest

from sdk.adapters.js_quix_payment_adapter import JSQuixPaymentAdapter
from sdk.adapters.network_adapter import NetworkAdapter
from sdk.enums.category import Category
from sdk.enums.country_code import CountryCodeAlpha3
from sdk.enums.currency import Currency
from sdk.enums.endpoints import Endpoints
from sdk.enums.environment import Environment
from sdk.exceptions.field_exception import MissingFieldException
from sdk.models.credentials import Credentials
from sdk.models.quix_models.quix_accommodation.auix_accommodation_cart_item import QuixAccommodationCartItem
from sdk.models.quix_models.quix_accommodation.auix_article_accommodation import QuixArticleAccommodation
from sdk.models.quix_models.quix_accommodation.quix_accommodation_pay_sol_extended_data import \
    QuixAccommodationPaySolExtendedData
from sdk.models.quix_models.quix_accommodation.quix_cart_accommodation import QuixCartAccommodation
from sdk.models.quix_models.quix_address import QuixAddress
from sdk.models.quix_models.quix_billing import QuixBilling
from sdk.models.quix_models.quix_flight.quix_cart_flight import QuixCartFlight
from sdk.models.quix_models.quix_flight.quix_flight_cart_item import QuixFlightCartItem
from sdk.models.quix_models.quix_flight.quix_article_flight import QuixArticleFlight
from sdk.models.quix_models.quix_flight.quix_flight_pay_sol_extended_data import QuixFlightPaySolExtendedData
from sdk.models.quix_models.quix_flight.quix_passenger_flight import QuixPassengerFlight
from sdk.models.quix_models.quix_flight.quix_segment_flight import QuixSegmentFlight
from sdk.models.quix_models.quix_product.quix_article_product import QuixArticleProduct
from sdk.models.quix_models.quix_product.quix_cart_product import QuixCartProduct
from sdk.models.quix_models.quix_product.quix_item_pay_sol_extended_data import QuixItemPaySolExtendedData
from sdk.models.quix_models.quix_product.quix_product_cart_item import QuixProductCartItem
from sdk.models.quix_models.quix_service.quix_article_service import QuixArticleService
from sdk.models.quix_models.quix_service.quix_cart_service import QuixCartService
from sdk.models.quix_models.quix_service.quix_service_cart_item import QuixServiceCartItem
from sdk.models.quix_models.quix_service.quix_service_pay_sol_extended_data import QuixServicePaySolExtendedData
from sdk.models.requests.quix_js.js_quix_accommodation import JSQuixAccommodation
from sdk.models.requests.quix_js.js_quix_flight import JSQuixFlight
from sdk.models.requests.quix_js.js_quix_item import JSQuixItem
from sdk.models.requests.quix_js.js_quix_service import JSQuixService
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


def read_xml_content(file_name):
    # Get the directory of the current file (test_notifications.py)
    current_file_directory = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the notifications directory relative to the current file
    xml_file_path = os.path.join(current_file_directory, 'notifications', file_name)

    if not os.path.exists(xml_file_path):
        raise FileNotFoundError(f"The file {xml_file_path} was not found.")

    with open(xml_file_path, 'r') as file:
        return file.read()


@pytest.fixture
def setup_credentials():
    credentials = Credentials()
    credentials.set_merchant_id(mock_configurations["merchantId"])
    credentials.set_merchant_pass(mock_configurations["merchantPassword"])
    credentials.set_environment(Environment.STAGING)
    credentials.set_product_id(mock_configurations["productId"])
    credentials.set_api_version(5)
    return credentials


def test_send_quix_js_items_on_success(setup_credentials, mocker):
    # Mock the network adapter send_request method
    mock_send_request = mocker.patch.object(NetworkAdapter, 'send_request',
                                            return_value=(200, read_xml_content('js_quix.json')))

    # Create the HostedPaymentRedirection object
    request = JSQuixItem()
    request.set_prepay_token("55354a9e-c121-41e7-863e-e58a7653499e")
    request.set_amount("99")
    request.set_customer_id("903")
    request.set_status_url("https://test.com/status")
    request.set_cancel_url("https://test.com/cancel")
    request.set_awaiting_url("https://test.com/await")
    request.set_success_url("https://test.com/sucess")
    request.set_error_url("https://test.com/error")
    request.set_customer_email("test@mail.com")
    request.set_customer_national_id("99999999R")
    request.set_dob("01-12-1999")
    request.set_first_name("Name")
    request.set_last_name("Last Name")
    request.set_ip_address("0.0.0.0")

    quix_article_product = QuixArticleProduct()
    quix_article_product.set_name("Nombre del servicio 2")
    quix_article_product.set_reference("4912345678903")
    quix_article_product.set_unit_price_with_tax(Decimal(99))
    quix_article_product.set_category(Category.DIGITAL)

    quix_item_cart_item_product = QuixProductCartItem()
    quix_item_cart_item_product.set_article(quix_article_product)
    quix_item_cart_item_product.set_units(1)
    quix_item_cart_item_product.set_auto_shipping(True)
    quix_item_cart_item_product.set_total_price_with_tax(Decimal(99))

    # Create items list and add quix_item_cart_item_product
    items: List[QuixProductCartItem] = [quix_item_cart_item_product]

    # Create QuixCartProduct and set its attributes using setters
    quix_cart_product = QuixCartProduct()
    quix_cart_product.set_currency(Currency.EUR)
    quix_cart_product.set_items(items)
    quix_cart_product.set_total_price_with_tax(Decimal('99'))

    # Create QuixAddress and set its attributes using setters
    quix_address = QuixAddress()
    quix_address.set_city("Barcelona")
    quix_address.set_country(CountryCodeAlpha3.ESP)
    quix_address.set_street_address("Nombre de la vía y nº")
    quix_address.set_postal_code("28003")

    # Create QuixBilling and set its attributes using setters
    quix_billing = QuixBilling()
    quix_billing.set_address(quix_address)
    quix_billing.set_first_name("Nombre")
    quix_billing.set_last_name("Apellido")

    # Create QuixItemPaySolExtendedData and set its attributes using setters
    quix_item_pay_sol_extended_data = QuixItemPaySolExtendedData()
    quix_item_pay_sol_extended_data.set_cart(quix_cart_product)
    quix_item_pay_sol_extended_data.set_billing(quix_billing)
    quix_item_pay_sol_extended_data.set_product("instalments")

    # Set paySolExtendedData for hostedQuixItem using setter
    request.set_pay_sol_extended_data(quix_item_pay_sol_extended_data)

    # Create the adapter and call the method
    adapter = JSQuixPaymentAdapter(setup_credentials)
    result = adapter.send_js_quix_item_request(request)

    # Check the response
    nemuru_cart_hash = result.get_notification().get_nemuru_cart_hash()
    nemuru_auth_token = result.get_notification().get_nemuru_auth_token()
    assert nemuru_cart_hash == "af24252b-e8c9-4fb2-9da2-7a476b2d8cd4"
    assert nemuru_auth_token == "62WBmZM44eDS2gZfVbgvEg5Cydea7IcY"

    # Capture the network call arguments
    mock_send_request.assert_called_once()
    call_args = mock_send_request.call_args
    json = call_args[1]['json']
    url = call_args[1]['url']
    # Verify the network call arguments
    assert json["merchantId"] == "111222"
    assert url == Endpoints.CHARGE_ENDPOINT_STG.value  # Change this to the correct endpoint


def test_send_quix_js_service_on_success(setup_credentials, mocker):
    mock_send_request = mocker.patch.object(NetworkAdapter, 'send_request',
                                            return_value=(200, read_xml_content('js_quix.json')))

    # Create the HostedPaymentRedirection object
    request = JSQuixService()
    request.set_prepay_token("55354a9e-c121-41e7-863e-e58a7653499e")
    request.set_amount("99")
    request.set_customer_id("903")
    request.set_status_url("https://test.com/status")
    request.set_success_url("https://test.com/success")
    request.set_error_url("https://test.com/fail")
    request.set_awaiting_url("https://test.com/await")
    request.set_cancel_url("https://test.com/cancel")
    request.set_customer_email("test@mail.com")
    request.set_customer_national_id("99999999R")
    request.set_dob("01-12-1999")
    request.set_first_name("Name")
    request.set_last_name("Last Name")
    request.set_ip_address("0.0.0.0")

    quix_article_service = QuixArticleService()
    quix_article_service.set_name("Nombre del servicio 2")
    quix_article_service.set_reference("4912345678903")
    quix_article_service.set_end_date("2024-12-31T23:59:59+01:00")
    quix_article_service.set_unit_price_with_tax(Decimal(99))
    quix_article_service.set_category(Category.DIGITAL)

    quix_item_cart_item_service = QuixServiceCartItem()
    quix_item_cart_item_service.set_article(quix_article_service)
    quix_item_cart_item_service.set_units(1)
    quix_item_cart_item_service.set_auto_shipping(True)
    quix_item_cart_item_service.set_total_price_with_tax(Decimal(99))

    items = [quix_item_cart_item_service]

    quix_cart_service = QuixCartService()
    quix_cart_service.set_currency(Currency.EUR)
    quix_cart_service.set_items(items)
    quix_cart_service.set_total_price_with_tax(Decimal('99'))

    quix_address = QuixAddress()
    quix_address.set_city("Barcelona")
    quix_address.set_country(CountryCodeAlpha3.ESP)
    quix_address.set_street_address("Nombre de la vía y nº")
    quix_address.set_postal_code("28003")

    quix_billing = QuixBilling()
    quix_billing.set_address(quix_address)
    quix_billing.set_first_name("Nombre")
    quix_billing.set_last_name("Apellido")

    quix_service_pay_sol_extended_data = QuixServicePaySolExtendedData()
    quix_service_pay_sol_extended_data.set_cart(quix_cart_service)
    quix_service_pay_sol_extended_data.set_billing(quix_billing)
    quix_service_pay_sol_extended_data.set_product("instalments")

    request.set_pay_sol_extended_data(quix_service_pay_sol_extended_data)

    # Create the adapter and call the method
    adapter = JSQuixPaymentAdapter(setup_credentials)
    result = adapter.send_js_quix_service_request(request)

    # Check the response
    nemuru_cart_hash = result.get_notification().get_nemuru_cart_hash()
    nemuru_auth_token = result.get_notification().get_nemuru_auth_token()
    assert nemuru_cart_hash == "af24252b-e8c9-4fb2-9da2-7a476b2d8cd4"
    assert nemuru_auth_token == "62WBmZM44eDS2gZfVbgvEg5Cydea7IcY"

    # Capture the network call arguments
    mock_send_request.assert_called_once()
    call_args = mock_send_request.call_args
    json = call_args[1]['json']
    url = call_args[1]['url']
    # Verify the network call arguments
    assert json["merchantId"] == "111222"
    assert url == Endpoints.CHARGE_ENDPOINT_STG.value  # Change this to the correct endpoint


def test_send_quix_hosted_accommodation_on_success(setup_credentials, mocker):
    mock_send_request = mocker.patch.object(NetworkAdapter, 'send_request',
                                            return_value=(200, read_xml_content('js_quix.json')))

    # Create the HostedPaymentRedirection object
    request = JSQuixAccommodation()
    request.set_prepay_token("55354a9e-c121-41e7-863e-e58a7653499e")
    request.set_amount("99")
    request.set_customer_id("903")
    request.set_status_url("https://test.com/status")
    request.set_cancel_url("https://test.com/cancel")
    request.set_awaiting_url("https://test.com/await")
    request.set_success_url("https://test.com/sucess")
    request.set_error_url("https://test.com/error")
    request.set_customer_email("test@mail.com")
    request.set_dob("01-12-1999")
    request.set_customer_national_id("99999999R")
    request.set_first_name("Name")
    request.set_last_name("Last Name")
    request.set_ip_address("0.0.0.0")

    quix_address = QuixAddress()
    quix_address.set_city("Barcelona")
    quix_address.set_country(CountryCodeAlpha3.ESP)
    quix_address.set_street_address("Nombre de la vía y nº")
    quix_address.set_postal_code("28003")

    quix_article_accommodation = QuixArticleAccommodation()
    quix_article_accommodation.set_name("Nombre del servicio 2")
    quix_article_accommodation.set_reference("4912345678903")
    quix_article_accommodation.set_checkin_date("2024-10-30T00:00:00+01:00")
    quix_article_accommodation.set_checkout_date("2024-12-31T23:59:59+01:00")
    quix_article_accommodation.set_guests(1)
    quix_article_accommodation.set_establishment_name("Hotel")
    quix_article_accommodation.set_address(quix_address)
    quix_article_accommodation.set_unit_price_with_tax(Decimal(99))
    quix_article_accommodation.set_category(Category.DIGITAL)

    quix_item_cart_item_accommodation = QuixAccommodationCartItem()
    quix_item_cart_item_accommodation.set_article(quix_article_accommodation)
    quix_item_cart_item_accommodation.set_units(1)
    quix_item_cart_item_accommodation.set_auto_shipping(True)
    quix_item_cart_item_accommodation.set_total_price_with_tax(Decimal(99))

    items = [quix_item_cart_item_accommodation]

    quix_cart_accommodation = QuixCartAccommodation()
    quix_cart_accommodation.set_currency(Currency.EUR)
    quix_cart_accommodation.set_items(items)
    quix_cart_accommodation.set_total_price_with_tax(Decimal(99))

    quix_billing = QuixBilling()
    quix_billing.set_address(quix_address)
    quix_billing.set_first_name("Nombre")
    quix_billing.set_last_name("Apellido")

    quix_accommodation_pay_sol_extended_data = QuixAccommodationPaySolExtendedData()
    quix_accommodation_pay_sol_extended_data.set_cart(quix_cart_accommodation)
    quix_accommodation_pay_sol_extended_data.set_billing(quix_billing)
    quix_accommodation_pay_sol_extended_data.set_product("instalments")

    request.set_pay_sol_extended_data(quix_accommodation_pay_sol_extended_data)

    # Create the adapter and call the method
    adapter = JSQuixPaymentAdapter(setup_credentials)
    result = adapter.send_js_quix_accommodation_request(request)

    # Check the response
    nemuru_cart_hash = result.get_notification().get_nemuru_cart_hash()
    nemuru_auth_token = result.get_notification().get_nemuru_auth_token()
    assert nemuru_cart_hash == "af24252b-e8c9-4fb2-9da2-7a476b2d8cd4"
    assert nemuru_auth_token == "62WBmZM44eDS2gZfVbgvEg5Cydea7IcY"

    # Capture the network call arguments
    mock_send_request.assert_called_once()
    call_args = mock_send_request.call_args
    json = call_args[1]['json']
    url = call_args[1]['url']
    # Verify the network call arguments
    assert json["merchantId"] == "111222"
    assert url == Endpoints.CHARGE_ENDPOINT_STG.value  # Change this to the correct endpoint


def test_send_quix_hosted_flights_on_success(setup_credentials, mocker):
    mock_send_request = mocker.patch.object(NetworkAdapter, 'send_request',
                                            return_value=(200, read_xml_content('js_quix.json')))

    # Create the HostedPaymentRedirection object
    request = JSQuixFlight()
    request.set_prepay_token("55354a9e-c121-41e7-863e-e58a7653499e")
    request.set_amount("99")
    request.set_customer_id("903")
    request.set_merchant_transaction_id("31122")
    request.set_status_url("https://test.com/status")
    request.set_cancel_url("https://test.com/cancel")
    request.set_awaiting_url("https://test.com/await")
    request.set_success_url("https://test.com/sucess")
    request.set_error_url("https://test.com/error")
    request.set_customer_email("test@mail.com")
    request.set_dob("01-12-1999")
    request.set_customer_national_id("99999999R")
    request.set_first_name("Name")
    request.set_last_name("Last Name")
    request.set_ip_address("0.0.0.0")

    quix_passenger_flight = QuixPassengerFlight()
    quix_passenger_flight.set_first_name("Pablo")
    quix_passenger_flight.set_last_name("Navvaro")

    passengers = [quix_passenger_flight]

    quix_segment_flight = QuixSegmentFlight()
    quix_segment_flight.set_iata_departure_code("MAD")
    quix_segment_flight.set_iata_destination_code("BCN")

    segments = [quix_segment_flight]

    quix_article_flight = QuixArticleFlight()
    quix_article_flight.set_name("Nombre del servicio 2")
    quix_article_flight.set_reference("4912345678903")
    quix_article_flight.set_departure_date("2024-12-31T23:59:59+01:00")
    quix_article_flight.set_passengers(passengers)
    quix_article_flight.set_segments(segments)
    quix_article_flight.set_unit_price_with_tax(Decimal(99))
    quix_article_flight.set_category(Category.DIGITAL)

    quix_item_cart_item_flight = QuixFlightCartItem()
    quix_item_cart_item_flight.set_article(quix_article_flight)
    quix_item_cart_item_flight.set_units(1)
    quix_item_cart_item_flight.set_auto_shipping(True)
    quix_item_cart_item_flight.set_total_price_with_tax(Decimal(99))

    items = [quix_item_cart_item_flight]

    quix_cart_flight = QuixCartFlight()
    quix_cart_flight.set_currency(Currency.EUR)
    quix_cart_flight.set_items(items)
    quix_cart_flight.set_total_price_with_tax(Decimal(99))

    quix_address = QuixAddress()
    quix_address.set_city("Barcelona")
    quix_address.set_country(CountryCodeAlpha3.ESP)
    quix_address.set_street_address("Nombre de la vía y nº")
    quix_address.set_postal_code("28003")

    quix_billing = QuixBilling()
    quix_billing.set_address(quix_address)
    quix_billing.set_first_name("Nombre")
    quix_billing.set_last_name("Apellido")

    quix_flight_pay_sol_extended_data = QuixFlightPaySolExtendedData()
    quix_flight_pay_sol_extended_data.set_cart(quix_cart_flight)
    quix_flight_pay_sol_extended_data.set_billing(quix_billing)
    quix_flight_pay_sol_extended_data.set_product("instalments")

    request.set_pay_sol_extended_data(quix_flight_pay_sol_extended_data)

    # Create the adapter and call the method
    adapter = JSQuixPaymentAdapter(setup_credentials)
    result = adapter.send_js_quix_flight_request(request)

    # Check the response
    nemuru_cart_hash = result.get_notification().get_nemuru_cart_hash()
    nemuru_auth_token = result.get_notification().get_nemuru_auth_token()
    assert nemuru_cart_hash == "af24252b-e8c9-4fb2-9da2-7a476b2d8cd4"
    assert nemuru_auth_token == "62WBmZM44eDS2gZfVbgvEg5Cydea7IcY"

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
    "customerId",
    "statusURL",
    "successURL",
    "errorURL",
    "awaitingURL",
    "cancelURL",
    "customerEmail",
    "merchantTransactionId",
    "customerNationalId",
    "dob",
    "firstName",
    "lastName",
    "ipAddress"
])
def test_missing_mandatory_field_throws_exception_hosted_quix_service(setup_credentials, missing_field):
    # Create the HostedQuixService object with all mandatory fields set
    request = JSQuixService()
    request.set_prepay_token("3123123-31easd-1344912-33111")
    request.set_amount("99")
    request.set_customer_id("903")
    request.set_status_url("https://test.com/status")
    request.set_success_url("https://test.com/success")
    request.set_error_url("https://test.com/fail")
    request.set_awaiting_url("https://test.com/await")
    request.set_cancel_url("https://test.com/cancel")
    request.set_customer_email("test@mail.com")
    request.set_merchant_transaction_id("333111")
    request.set_customer_national_id("99999999R")
    request.set_dob("01-12-1999")
    request.set_first_name("Name")
    request.set_last_name("Last Name")
    request.set_ip_address("0.0.0.0")

    quix_article_service = QuixArticleService()
    quix_article_service.set_name("Nombre del servicio 2")
    quix_article_service.set_reference("4912345678903")
    quix_article_service.set_end_date("2024-12-31T23:59:59+01:00")
    quix_article_service.set_unit_price_with_tax(Decimal(99))
    quix_article_service.set_category(Category.DIGITAL)

    quix_item_cart_item_service = QuixServiceCartItem()
    quix_item_cart_item_service.set_article(quix_article_service)
    quix_item_cart_item_service.set_units(1)
    quix_item_cart_item_service.set_auto_shipping(True)
    quix_item_cart_item_service.set_total_price_with_tax(Decimal(99))

    items = [quix_item_cart_item_service]

    quix_cart_service = QuixCartService()
    quix_cart_service.set_currency(Currency.EUR)
    quix_cart_service.set_items(items)
    quix_cart_service.set_total_price_with_tax(Decimal('99'))

    quix_address = QuixAddress()
    quix_address.set_city("Barcelona")
    quix_address.set_country(CountryCodeAlpha3.ESP)
    quix_address.set_street_address("Nombre de la vía y nº")
    quix_address.set_postal_code("28003")

    quix_billing = QuixBilling()
    quix_billing.set_address(quix_address)
    quix_billing.set_first_name("Nombre")
    quix_billing.set_last_name("Apellido")

    quix_service_pay_sol_extended_data = QuixServicePaySolExtendedData()
    quix_service_pay_sol_extended_data.set_cart(quix_cart_service)
    quix_service_pay_sol_extended_data.set_billing(quix_billing)
    quix_service_pay_sol_extended_data.set_product("instalments")

    request.set_pay_sol_extended_data(quix_service_pay_sol_extended_data)

    # Remove the specified mandatory field by setting it to None using setattr
    setattr(request, f"_QuixHostedRequest__{missing_field}", None)

    # Create the adapter
    adapter = JSQuixPaymentAdapter(setup_credentials)

    # Check if the is_missing_field method returns the correct missing field
    with pytest.raises(MissingFieldException) as exc_info:
        adapter.send_js_quix_service_request(request)

    assert str(exc_info.value) == f"Missing {missing_field}"


@pytest.mark.parametrize("missing_field", [
    "name",
    "reference",
    "end_date",
    "unit_price_with_tax",
    "category"
])
def test_missing_mandatory_field_throws_exception_quix_article_service(missing_field):
    # Create the QuixArticleService object with all mandatory fields set
    quix_article_service = QuixArticleService()
    quix_article_service.set_name("Nombre del servicio 2")
    quix_article_service.set_reference("4912345678903")
    quix_article_service.set_end_date("2024-12-31T23:59:59+01:00")
    quix_article_service.set_unit_price_with_tax(Decimal(99))
    quix_article_service.set_category(Category.DIGITAL)

    # Remove the specified mandatory field by setting it to None using setattr
    setattr(quix_article_service, f"_QuixArticleService__{missing_field}", None)

    # Check if the is_missing_field method returns the correct missing field
    if missing_field == "unit_price_with_tax":
        with pytest.raises(TypeError, match=r"'<=' not supported between instances of 'NoneType' and 'int'"):
            quix_article_service.is_missing_field()
    else:
        is_missing, field = quix_article_service.is_missing_field()
        assert is_missing
        assert field == missing_field


@pytest.mark.parametrize("missing_field", [
    "article",
    "units",
    "total_price_with_tax"
])
def test_missing_mandatory_field_throws_exception_quix_service_cart_item(missing_field):
    # Create the QuixServiceCartItem object with all mandatory fields set
    quix_article_service = QuixArticleService()
    quix_article_service.set_name("Nombre del servicio 2")
    quix_article_service.set_reference("4912345678903")
    quix_article_service.set_end_date("2024-12-31T23:59:59+01:00")
    quix_article_service.set_unit_price_with_tax(Decimal(99))
    quix_article_service.set_category(Category.DIGITAL)

    quix_item_cart_item_service = QuixServiceCartItem()
    quix_item_cart_item_service.set_article(quix_article_service)
    quix_item_cart_item_service.set_units(1)
    quix_item_cart_item_service.set_auto_shipping(True)
    quix_item_cart_item_service.set_total_price_with_tax(Decimal(99))

    # Remove the specified mandatory field by setting it to None using setattr
    setattr(quix_item_cart_item_service, f"_QuixServiceCartItem__{missing_field}", None)

    # Check if the is_missing_field method returns the correct missing field
    if missing_field == "units" or missing_field == "total_price_with_tax":
        with pytest.raises(TypeError, match=r"'<=' not supported between instances of 'NoneType' and 'int'"):
            quix_item_cart_item_service.is_missing_field()
    else:
        is_missing, field = quix_item_cart_item_service.is_missing_field()
        assert is_missing
        assert field == missing_field


@pytest.mark.parametrize("missing_field", [
    "currency",
    "items",
    "total_price_with_tax"
])
def test_missing_mandatory_field_throws_exception_quix_cart_service(missing_field):
    # Create the QuixCartService object with all mandatory fields set
    quix_article_service = QuixArticleService()
    quix_article_service.set_name("Nombre del servicio 2")
    quix_article_service.set_reference("4912345678903")
    quix_article_service.set_end_date("2024-12-31T23:59:59+01:00")
    quix_article_service.set_unit_price_with_tax(Decimal(99))
    quix_article_service.set_category(Category.DIGITAL)

    quix_item_cart_item_service = QuixServiceCartItem()
    quix_item_cart_item_service.set_article(quix_article_service)
    quix_item_cart_item_service.set_units(1)
    quix_item_cart_item_service.set_auto_shipping(True)
    quix_item_cart_item_service.set_total_price_with_tax(Decimal(99))

    items = [quix_item_cart_item_service]

    quix_cart_service = QuixCartService()
    quix_cart_service.set_currency(Currency.EUR)
    quix_cart_service.set_items(items)
    quix_cart_service.set_total_price_with_tax(Decimal('99'))

    # Remove the specified mandatory field by setting it to None using setattr
    setattr(quix_cart_service, f"_QuixCartService__{missing_field}", None)

    # Check if the is_missing_field method returns the correct missing field
    if missing_field == "total_price_with_tax":
        with pytest.raises(TypeError, match=r"'<=' not supported between instances of 'NoneType' and 'int'"):
            quix_cart_service.is_missing_field()
    else:
        is_missing, field = quix_cart_service.is_missing_field()
        assert is_missing
        assert field == missing_field


@pytest.mark.parametrize("missing_field", [
    "city",
    "country",
    "street_address",
    "postalCode"
])
def test_missing_mandatory_field_throws_exception_quix_address(missing_field):
    # Create the QuixAddress object with all mandatory fields set
    quix_address = QuixAddress()
    quix_address.set_city("Barcelona")
    quix_address.set_country(CountryCodeAlpha3.ESP)
    quix_address.set_street_address("Nombre de la vía y nº")
    quix_address.set_postal_code("28003")

    # Remove the specified mandatory field by setting it to None using setattr
    setattr(quix_address, f"_QuixAddress__{missing_field}", None)

    # Check if the is_missing_field method returns the correct missing field
    is_missing, field = quix_address.is_missing_field()
    assert is_missing
    assert field == missing_field
