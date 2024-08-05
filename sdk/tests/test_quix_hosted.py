from decimal import Decimal
from typing import List

import pytest

from sdk.adapters.hosted_quix_payment_adapter import HostedQuixPaymentAdapter
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
from sdk.models.requests.quix_hosted.hosted_quix_accommodation import HostedQuixAccommodation
from sdk.models.requests.quix_hosted.hosted_quix_flight import HostedQuixFlight
from sdk.models.requests.quix_hosted.hosted_quix_item import HostedQuixItem
from sdk.models.requests.quix_hosted.hosted_quix_service import HostedQuixService
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


def test_send_quix_hosted_items_redirect_url_on_success(setup_credentials, mocker):
    # Mock the network adapter send_request method
    mock_send_request = mocker.patch.object(NetworkAdapter, 'send_request', return_value=(200, "http://redirect.url"))

    # Create the HostedPaymentRedirection object
    request = HostedQuixItem()
    request.set_amount("99")
    request.set_customer_id("903")
    request.set_status_url("https://test.com/status")
    request.set_cancel_url("https://test.com/cancel")
    request.set_awaiting_url("https://test.com/await")
    request.set_success_url("https://test.com/sucess")
    request.set_error_url("https://test.com/error")
    request.set_merchant_transaction_id("333111")
    request.set_customer_email("test@mail.com")
    request.set_customer_national_id("99999999R")
    request.set_merchant_transaction_id("34441")
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
    adapter = HostedQuixPaymentAdapter(setup_credentials)
    result = adapter.send_hosted_quix_item_request(request)

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
    assert query_parameters["encrypted"] == ("Z8/GfPAdBmFNRD1Lf2f+YMia/i1YHDOSu3pUAn8zRG9c94O/G8WqcWdQFTTLkT1"
                                             "uSoS41W0J8Qkw8rcoGl3KQxAPrZ6K2aLfX5TSlnYt6oV6yHv5Rc4+o5XFqW66KbO"
                                             "1Ev7dgEsitzr93dkRDxtiVW5wPCGZyk1OELQGXx/ojd31yzUiRBxOvegWrZWOHqc"
                                             "qUVrOFx4SkChWCuiMTk3pyFfDWJMGPaQkK8ALgms4X4tetSmIgohHxt+kR2MelC4O"
                                             "Qa8zc43+gYi7mYcokRa5aWV+Yc+xU1OBxXqFnrgidtHwlYTRFuS8haEsmZr99cSK2V"
                                             "Q78/PedsygBYLK0Mh3vEqOHivnF8m5KqamAzWQLVm5TEKRKy5fA7HqxaDg3yGVWxTr"
                                             "fQtLasxsRIzrGktxF55MAQO2fnMFCfknbP6+eGYj1sXLFiPxv3g0lXadUPqOj6sJRie"
                                             "zQJGpPPmWNlrZll9yHiZM/BFcpWeKHNrZxUnnBucVgM4LeqH0seG9DXFhhflrpzAhaA7"
                                             "rEqj6l1uruVwzRMkin/cvKUsHXt2ZxgWeXpyTKyporbTewmXyfmpE2sO5BDVYJKE9I8c"
                                             "1tnVexBI6NlWZ6rPckmlRNjiPLcb9yNLj+yCocWwI5n3HaxyIZCFaempbWKhCGtTeJF2"
                                             "G5ZGTi4Tk888+tlhd5JKkoq0NIQs4lE/AAm/4fnQj2CjDBE4ocxyS7OAOrjmU/y84ONXJ"
                                             "cUyZv5tpZM6at/JuIMgFtLY1aQdjiZrF7DogoZgHIS88uHO+yCL+KILd/VNtIfHfO88bd"
                                             "nFU7BRXA6D+jMpCyovNxHmFwa2M16IiFS0woBGIniIQThHE26E8N9QTmgqe6mOZ192E8a"
                                             "igQJZ/6xhH42hhAM9/bGra95G/2clwVmkyUopXvdm7Yjm/VWyiZPdNDJijbiMRBunhLlO"
                                             "JfEl7T8roTNx7jydkh2AStjeqzvw4sdA/kcG5Ped6qukmtfhAhfZQFvRNoFHnJGT7flb8"
                                             "lXnvrcHsmr94uQPKOki6AQ81UG3u+eqULToHPEd3RxEETj/LUSJTMALcg4bp38mGyY7St"
                                             "6c7LFtdtktsfFjYAs4xH34nXa+SnM0I6kcktR/wiiznkmAhBSzHFwjfnlF+5hdF4hGXtRG"
                                             "THaAvzft7nv38w7dA5X8+MlF4CdZhpBMpjUGVxDrDdPep5pDwZimxaGfGlN+A7I43bb2y9"
                                             "nUMjaUDrWyyljnA5MoAi8ZDd8uP5aKbBqX/Q+uIwUhBchYJfoUlauZRblH3khr+i8NYL8uD"
                                             "Q3DlVb7WpV78F67MAwo8nhXMNMhSuhGcxVfVVYXqm45xmQBM0s9crg76VHg7i2HSZvMN7QJ"
                                             "jzk+YLo9kKpz2YOSaaO7aJmhMyD9BQw2bILMHUfG4qe82xKlehwj6aPbF0SUGi3kfZlVPku"
                                             "xSMB95Wxn5BNQxE9vqOwmE6FbDkkzRniaEKNCdEiCLk2SRzr8rvbD5xqVfuhtk6pTgkSR/"
                                             "2opBMfrsdmJBS/S9mn79Vbqq/w0oPUdoGOJEyRr8xYxx/rmi39NeVoqPW3a+44zY9KAZJ13v"
                                             "5EqeuAqQ/8bKRle/xmXBwkkcDGNQbmW+4okxcx85uGysRbgq+TVm7oGnkaKLNj0DpmUEVlqH"
                                             "jn7VEy6Ief9vL5iZbU0qhUfqp04/MHmV3j5LQ4/+XdH8BeU/z8u85hi/NUlFYPkP0HAn4Go"
                                             "DxDsEv7ABX/Dg0bOt4SCzXWxjNCaf0FXslJEjMQrDSSFtUW2KXUtx89kDkPfRGXX4pGfofO"
                                             "lvWNmFT2lTJbNtv8bhH1xROo6ImmA3orJIKJAIWOU1C6idi3T8M1X94"
                                             "/VkIzk5Q3ph5lMclGfp")

    assert query_parameters["integrityCheck"] == "34418c13f2f7f49ec76597875d070b1f56d1df68b19f780bc7dabbc3f6f45676"
    assert url == Endpoints.HOSTED_ENDPOINT_STG.value  # Change this to the correct endpoint


def test_send_quix_hosted_service_redirect_url_on_success(setup_credentials, mocker):
    # Mock the network adapter send_request method
    mock_send_request = mocker.patch.object(NetworkAdapter, 'send_request', return_value=(200, "http://redirect.url"))

    # Create the HostedPaymentRedirection object
    request = HostedQuixService()
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

    # Create the adapter and call the method
    adapter = HostedQuixPaymentAdapter(setup_credentials)
    result = adapter.send_hosted_quix_service_request(request)

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
    assert query_parameters["encrypted"] == (
        "Z8/GfPAdBmFNRD1Lf2f+YMia/i1YHDOSu3pUAn8zRG9c94O/G8WqcWdQFTTLkT1uSoS41W0J8Q"
        "kw8rcoGl3KQxAPrZ6K2aLfX5TSlnYt6oVI/VwGX3zXuX4xmZF0zJacBbFXFrmZlAANkf3+c6y"
        "MoyUgGhtHNtBdk2LC40jensHCSjDbbPRWYjWyfkn2TdMUSho0oBLNj+XSSo/xa/rezGBiM1RL"
        "pZUw9Trii++ZF6p3IbTcE9rkUt4XnrfccxISSZoktCOMlS5rjT/IAeQ4HaWEl8jm+V/VtdmcL"
        "JejN8LpV7WbNht0OfETT4VBH6ewIBVtsZSbCqEzfnOIo5NbHmkcQWdaB1gWd1XRY+dJB++yvo"
        "CacYwSMQ7vPa4kDyVKW4xMnOyi33+kPJSYw1Ba1rnHuzUs0/ssCkDK0GTcBun9CVDgrdAnAiGr"
        "M88Bx1PSYRTfp0Gr+C536I1+lKpxEiJXop+9bywieS8rztUUQ2HtQJPGDui/JBk68xylckCR9Wb"
        "xndD2+S5UlYZre8/0N5Di/3Vhz5eeH29Xel42ZNPiFoEeFdYkKk96lJdzIMQU4YmZqN6uCCNje"
        "lOlL0H1L11CqLy70YPN+LHynNDRUGa5a2iW6MhUKEnur1m1vGnsKdl5eFE0FeaqqI8Drlp33oAd"
        "KVdRMsFHOrrNENhqHhhJNTBfkK0ELcT7v8BuYwRZaWBSDtWIVa4r8ZzQa0Pq7jjBwV29cvWiXc"
        "gKjZjqoCJUWVFsmArIgwiO8iAHbC6qKc0NQdm+LTl1vqUOoFnmxdJfDlrZFbYtq8O5wQq0mZoWt"
        "Wb9NpEeyTHQDkk1n0QO+5ngt+EaSeK9H5bGFdqoJ/gg494e9Yek9jFJZoBk/gAVlXRBTtWaUbEwx"
        "+XidQk+PLD0MA6FO6LxuFJqUPxQCAWduBCoS1iYU7pYSK0gYm079zADaYsJsz8fG9MlCSjYnzS3"
        "M+uUwoAA14g8XIW5q9DEHYFwpVt20dndIer3NAIBkMvZFLURi0IbTfrNXgs+xyM1fqe/EA4BpS7W"
        "KQtvDFiBVqzBAeg9xbThXr4ylby27wg+TOQMZwRgj6Hz3GQAn8CXfwArXKBDkJ5BVaXcrMHfMLN+"
        "Cr4TbOATYyrlLPfRwXhPVBBvJtUhOuk9wrcD9j/w1JPIQrr5eSljwCPqG4HyHBfkasDDuskBg03B"
        "lKc7PELAWnOeKk8JdFvf7JOcHHI6Q5oikle4gi5a5KPoyInut834DqGIvcgAZM6/FxFlOPqAz6Uxp"
        "G9/UEEhXc1nSQqh/5Q10BtWHo2JmJTpXFsj8hc+Gu5HQyC8/Tr+qXL5AO9INHTCk9HKtMp+c5+nOh"
        "H+bft550QLBlS5xkepZIBkf84lvEmvk/rLTbYPsyQTsbPAis72g7nPNry/qI0sd95/Op3tt5ekr+F"
        "clD02lHljzA76AoUhPjFZlY2MP2ew2MnH9iCEJAXKhqfFUj8GC1oUzl2KHQGG4HEZC1XIggS8BKlDC"
        "yPZXBTvX3vLJub5Eiiq0emjs0bPUv/1hnL7KnddID45ARKfJRXE8WOMarrrZGW164dF8JhJ/C7GNIx9"
        "WV7XKzSYQac0hdUoyyDWOC7on2/B75xIT2xKh7fYo+Nq+FPc1Uc4E9LkBN4C23smNyxjzDwHW+OkAXs"
        "gjCo0MESOFVnHSAQhpLbW/pkAOsK9i1CtWqsvI5IrIOlz00RwK0OCmP6izSUA9FZjC3ygqMhqSNFJts"
        "4JiU/WWKnL32I5x755uN2/vlA6DfJ5J72snmt6TuP4sPTSvCDKtcwp3hT/zgAdfg3grVgWVy47rUbPK"
        "OsSNO3kFbJe8Cz/+hp2o3hUtCXjfOqn7UaeSBOPj7U7kmgDwOrTfwH4/a+5DofG/r9T5/UYMDewfbe/"
        "HaBhQd+CqiT/ha0XNN+caGIlmSe45VBYSSfcIZNm99N1bg==")

    assert query_parameters["integrityCheck"] == "e6d8ce43e8c2532519ba730937c8cbae08085386b439200c24d6df7f977a355a"
    assert url == Endpoints.HOSTED_ENDPOINT_STG.value  # Change this to the correct endpoint


def test_send_quix_hosted_accommodation_redirect_url_on_success(setup_credentials, mocker):
    # Mock the network adapter send_request method
    mock_send_request = mocker.patch.object(NetworkAdapter, 'send_request', return_value=(200, "http://redirect.url"))

    # Create the HostedPaymentRedirection object
    request = HostedQuixAccommodation()
    request.set_amount("99")
    request.set_customer_id("903")
    request.set_merchant_transaction_id("333111")
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
    adapter = HostedQuixPaymentAdapter(setup_credentials)
    result = adapter.send_hosted_quix_accommodation_request(request)

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
    assert query_parameters["encrypted"] == ("Z8/GfPAdBmFNRD1Lf2f+YMia/i1YHDOSu3pUAn8zRG9c94O/G8WqcWdQFTTLkT1uSoS41W0"
                                             "J8Qkw8rcoGl3KQxAPrZ6K2aLfX5TSlnYt6oVI/VwGX3zXuX4xmZF0zJacBbFXFrmZlAANk"
                                             "f3+c6yMoyUgGhtHNtBdk2LC40jensHCSjDbbPRWYjWyfkn2TdMUSho0oBLNj+XSSo/xa/re"
                                             "zGBiM1RLpZUw9Trii++ZF6qR4xWsjP027jFUocySMEHG78hn16O5tbpygZ/0fAhbz5uo6N9"
                                             "f6IN1dn3/+hk8/ub79agg3CsFEypRKDNaij/Fql+D1Yh6kFJfaI5IUw7KXICjs6RfrcD3/e"
                                             "dQ9+hPM/x3wsRmNApBEsqAVwTrX6BlFQjMqTxsIaWtJidNCmcZ648MLxgtO0kkyj1clRk27T"
                                             "Im8xg1j10L+qHTowztJy6miPd4PXT9QSt+ZBtTWXi1MHMDQEIhAOMVjIyyRZqcd1wlGIGPlh"
                                             "ja5Pgrbs0G/7iI1+/srjcCeRVzT/UX9URYz78b2DOksDxUxIbpwjuiMkoqfwlZ6FXZuTW2iqg"
                                             "oKDUzVHrR7RupqqQs1nv2gojWm97khTAS1MNGZqShEZi/chPKBJ+JUIPTBahP4q8FaUTM/MJ"
                                             "kY6llCaiUyc+L5ohY4R+wgFX4OIy5ild9ELWFcvtqoWOf/UvH58D6UPYaSs6OYQu2UoETG"
                                             "AsF62YFoIYWm0Dn1TUjTwtAcyvFKfacTUFP9+wf6A6QRsczpMLtxD6hhSuLvt0JhYdrhOL4"
                                             "bAtmGABkY/T1OdkBLwY/ibW46ZLVfGGeDna5afn0wsuNtfNxgqPd+FhsXm7AsyGn/4p3vRM"
                                             "UZlxWb1xdQzjdlOQBq765+t9cFJbp86YhWfTWqOZJ5YEomdB1M9uxxDntc3GYos87VW2ouz"
                                             "or2e4A2FgEZtqPWbnvAsa0vZg6eOstKxp+NpuMa1Bnu3iZHua9mL9QIX+AmzB336FSLgnwS"
                                             "7Ak9eaQLLinUGm93A2PYP+5DoyKu9b/ineccYr7lZTTpawZYIgYcnf2FQJk+YuYaUStNCXO"
                                             "LRdLn6YdFL3M8oLGQ790U7uLcrlXC/ZqGapznUqrZGUosPH3m/NayYGqaNIuK9t5tJev1rz"
                                             "aq0J1ePeVaMGO9RK9DkxypmkkkJt//yREvrILwOZjY2ZtC7cwxu/8w3711LCX9QBOnc/XmR"
                                             "jWpRYQze/iknVo1gMfC/8e0s1nkW/T6lD+ph6GqZRP+ezTD928V5BeYSpNAy5KejC8eZp1eR"
                                             "PUCUi1y7/xvUnLSNvGgSOYaLohrG9PaRYa+fMaWlXRuqn0eTUbKdQpdSNg0/nRbCbT2FohT"
                                             "UqR5TRhakCuboy+xiF2M7e1pckNcPl9KsdXeEBC2sIhS3rGWT7ws52A+I68/Lxe463DuWIL"
                                             "ZJGFvUdlpTc5y1UHTKP2iSbZ/eJ5BnONZEPms1pjuZ7KEA8tof6dOKLg6h5dzxCJ4LLpu9r"
                                             "qDVKIor0F3vmjIPk+iERtQvDWAXu0QNGLjJthjd17zv6iu8Bpoa4zsPuW7eYzm1Xz6n/3TJ"
                                             "wpJ+wYACzOJX3TpjW5mKlR6XqshdCS8MLIYN+483v65OD3/oCVh/kphexV7eDVBEt6teTYo"
                                             "9rQavuoIm4gyxFE0zBB0sDyygI0UY8gD1b1tU2IalPxyKkPmmX3yv09UB93zwAk4uYuHCJr"
                                             "77Ddz93Z7eEjVmiizKWwbI/8ZiqdQvYK7snqnboTt7bSjfg/zPvLq+BIVDWHl7I0AAqSTx"
                                             "N4QosmuayuO5b9dFECQNA20HMbdErEN3ck/EoHV+8iF4ogzJ5egIMnsCNJKDraN2Q7gKjk"
                                             "WHpkKrnfcupLbsJSK0ctemfe5o5C1MZnUPaUYfyop0QoEpnni2bwBcUQA/gMHHhcsLBxkg/"
                                             "padh6wP9uvWYd+bGMHn994766bYicUEJwwUDPjduw+mWSnq20w4c765NJkV3sTG0QY5lsMC"
                                             "ASDgggJrjAjC0TUf6MzeRozYDgxiL5m8mdCj9PIOXrEIMF3tH5zRzHqQkWKtw4FjCGparth"
                                             "pGBUo3FpFVl3nzmvTsW3Q+LMXPDQz0K1NNVy0oQjuqgqdJepxB6veT6ti2zXvSGh27Jq2Lvs"
                                             "Q1XRhfZy9w5LZuso1J7OqCZ/QFxIjMpEClnxFMuk1QFeiHwjbMzJdLDW3lzKjqXFNuW9E/8"
                                             "4/qJe9hyz0rfiD3SE8GkorbDLZmKU8bfOvouH9BB2HjGlOV7mvZeG+8zZQLoMC8RE0WSiGCs"
                                             "EljTVsA1ECfXXWlG8EgSTXciov1VHomlK1J08V28m6iSH0qIooo15W7pp8k97+RPQo0vAud"
                                             "ql9ZIjOWsEZsLOmP+5BPyXERmReW+oMgEheOJyK9wZ0MRFyyC0Vj/X5Nu9MRaV3Y=")

    assert query_parameters["integrityCheck"] == "5261658ff67bb68887a99426ad1b19cf49ce4e03748cef1d7402901acd714e9b"
    assert url == Endpoints.HOSTED_ENDPOINT_STG.value  # Change this to the correct endpoint


def test_send_quix_hosted_flight_redirect_url_on_success(setup_credentials, mocker):
    # Mock the network adapter send_request method
    mock_send_request = mocker.patch.object(NetworkAdapter, 'send_request', return_value=(200, "http://redirect.url"))

    # Create the HostedPaymentRedirection object
    request = HostedQuixFlight()
    request.set_amount("99")
    request.set_customer_id("903")
    request.set_status_url("https://test.com/status")
    request.set_cancel_url("https://test.com/cancel")
    request.set_awaiting_url("https://test.com/await")
    request.set_success_url("https://test.com/sucess")
    request.set_error_url("https://test.com/error")
    request.set_customer_email("test@mail.com")
    request.set_merchant_transaction_id("333111")
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
    quix_article_flight.set_unit_price_with_tax(99)
    quix_article_flight.set_category(Category.DIGITAL)

    quix_item_cart_item_flight = QuixFlightCartItem()
    quix_item_cart_item_flight.set_article(quix_article_flight)
    quix_item_cart_item_flight.set_units(1)
    quix_item_cart_item_flight.set_auto_shipping(True)
    quix_item_cart_item_flight.set_total_price_with_tax(99)

    items = [quix_item_cart_item_flight]

    quix_cart_flight = QuixCartFlight()
    quix_cart_flight.set_currency(Currency.EUR)
    quix_cart_flight.set_items(items)
    quix_cart_flight.set_total_price_with_tax(99)

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
    adapter = HostedQuixPaymentAdapter(setup_credentials)
    result = adapter.send_hosted_quix_flight_request(request)

    # Check the response
    response_url = result.get_redirect_url()
    assert response_url == "http://redirect.url"

    # Capture the network call arguments
    mock_send_request.assert_called_once()
    call_args = mock_send_request.call_args
    headers = call_args[1]['headers']
    query_parameters = call_args[1]['query_parameters']
    json = call_args[1]['json']
    url = call_args[1]['url']
    print(query_parameters["integrityCheck"])
    # Verify the network call arguments
    assert headers["apiVersion"] == "5"
    assert headers["encryptionMode"] == "CBC"
    assert headers["iv"] == encoded_iv
    assert query_parameters["merchantId"] == "111222"
    assert query_parameters["encrypted"] == ("Z8/GfPAdBmFNRD1Lf2f+YMia/i1YHDOSu3pUAn8zRG9c94O/G8WqcWdQFTTLkT1uSoS"
                                             "41W0J8Qkw8rcoGl3KQxAPrZ6K2aLfX5TSlnYt6oVI/VwGX3zXuX4xmZF0zJacBbFXF"
                                             "rmZlAANkf3+c6yMoyUgGhtHNtBdk2LC40jensHCSjDbbPRWYjWyfkn2TdMUSho0oBL"
                                             "Nj+XSSo/xa/rezGBiM1RLpZUw9Trii++ZF6qR4xWsjP027jFUocySMEHG78hn16O5t"
                                             "bpygZ/0fAhbz5uo6N9f6IN1dn3/+hk8/ub79agg3CsFEypRKDNaij/Fql+D1Yh6kFJ"
                                             "faI5IUw7KXICjs6RfrcD3/edQ9+hPM/x3wsRmNApBEsqAVwTrX6BlFQjMqTxsIaWtJ"
                                             "idNCmcZ648MLxgtO0kkyj1clRk27TIm8xg1j10L+qHTowztJy6miPd4PXT9QSt+ZBtT"
                                             "WXi1MHMDQEIhAOMVjIyyRZqcd1wlGIGPlhja5Pgrbs0G/7iI1+/srjcCeRVzT/UX9UR"
                                             "Yz78b2DOksDxUxIbpwjuiMkoqfwlZ6FXZuTW2iqgoKDUzVHrR7RupqqQs1nv2gojWm9"
                                             "7khTAS1MNGZqShEZi/chPKBJ+JUIPTBahP4q8FaUTM/MJkY6llCaiUyc+L5ohY4R+wg"
                                             "FX4OIy5ild9ELWFcvtqoWOf/UvH58D6UPYaSs6OYQu2UoETGAsF62YFoIYWm0Dn1TUj"
                                             "TwtAcyvFKfacTUFP9+wf6A6QRsczpMLtxD6hhSuLvt0JhYdrhOL4bAtmGABkY/T1Odk"
                                             "BLwY/ibW46ZLVfGGeDna5afn0wsuNtfNxgqPd+FhsXm7AsyGn/4p3vRMUZlxWb1xdQz"
                                             "jdlOQBq765+t9cFJbp86YhWfTWqOZJ5YEomdB1M9uxxDntc3GYos87VW2ouzor2e4A2"
                                             "FgEZtqPWbnvAsa0vZg6eOstKxp+NpuMa1Bnu3iZHua9mL9QIX+AmzB336FSLgnwS7Ak"
                                             "9eaQLLinUGm93A2PYP+5DoyKu9b/ineccYr7lZTTpawZYIgYcnf2FQJk+YuYaUStNCX"
                                             "OLRdLn6YdFL3M8oLGQ790U7uLcrlXC/ZqGapznUqrZGUosPH3m/NayYGqaNIuK9t5tJ"
                                             "ev1rzaq0J1ePeVaMGO9RK9DkxypmkkkJt//yREvrILwOZjY2ZtC7cwxu/8w3711LCX9"
                                             "QBOnc/XmRjWpRYQze/iknVo1gMfC/8e0s1nkW/T6lD+ph6GqZRP+ezTD928V5BeYSpN"
                                             "Ay5KejC8eZp1eRPUCUi1y7/xvUnLSNvGgSOYaLohrG9PaRYa+fMaWlXRuqn0eTUbKdQ"
                                             "pdSNg0/nRbCbT2FohTUqR5TRhakCuboy+xiF2M7e1pckNcPl9KsdXeEBC2sIhS3rGWT"
                                             "7ws52A+I68/Lxe463DuWILZJGFvUdlpTc5y1UHTKP2iSbZ/eJ5BnONZEPms1pjuZ7KE"
                                             "A8tof6dOKLg6h5dzxCJ4LLpu9rqDVKIor0F3vmjIPk+iERtQvDWAXu0QNGLjJthjd17"
                                             "zv6iu8Bpoa4zsPuW7eYzm1Xz6n/3TJwpJ+wYACzOJX3TpjW5mKlR6XqshdCS8MLIYN+"
                                             "483v65OD3/oCVh/kphbbh3v9v62XrWpHnyzw+Z6DjSZZNoR4xB7ly2weVTZ9SFbcO9OM"
                                             "DbNac5wJ+aNOYnWo9C2HyCMQ+5bVCXnA98v4wu8IafopMDxywKA2CppqZ6BL9NgTkAJJ"
                                             "7YfpJ12BNY85NdY16ArtkWz97wRBPfOT3br3H06YFz+jK9jAgcqg+A6/1URK0dJ/4Ohm"
                                             "zokBOIdiYbgVfP91GmHrg25nddy3qbVbsjNgeo+So9en4OPZvCsfNYFrsJHJoS8jwn8Q"
                                             "NXFtLHIAp6v9RlTDew7m1Bvsh3Ccvtzl4y9mLSgthJjp53lYdOht0C1qxXHwq4WXipDv"
                                             "b5yrq8tU+Z/9DkJHC4xGBbRguqrAsLOJU10wY6LK5P0Jxh0PpPuhF60NG0C/WXnK54OEt"
                                             "C58v5w/YmJoPTH0Ww/dQjYxxkvSIW89RLCcJw4Jo/EE9l7UJnIgvYMWBDVdnxcqBCynU"
                                             "eI2D96bHB1moKbdBBScHmrtGcVoC+19PRzOV94dey2NzaR4YCRKfB+DzGDEWl5TTtYU5xh"
                                             "hMaRfwSV0Bp+02UJUe4E2suWyHVSNNF5EuRqfbO/t6Go+/k3f3EORelczgjbJp2n/2K9o=")

    assert query_parameters["integrityCheck"] == "d91311cd71f4dc28968e58f9da0c9b38d41edbd578f814736040d5f202eba6fc"
    assert url == Endpoints.HOSTED_ENDPOINT_STG.value  # Change this to the correct endpoint


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
    request = HostedQuixService()
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
    adapter = HostedQuixPaymentAdapter(setup_credentials)

    # Check if the is_missing_field method returns the correct missing field
    with pytest.raises(MissingFieldException) as exc_info:
        adapter.send_hosted_quix_service_request(request)

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
