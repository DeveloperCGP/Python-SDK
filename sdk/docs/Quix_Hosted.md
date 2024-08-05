# Quix Hosted

## Table of Contents

- [Common Prerequisite: Creating Credentials Object](#common-prerequisite-creating-credentials-object)
  - [Steps](#steps)
- [Quix Hosted Items Request](#quix-hosted-items-request)
  - [Step 1: Refer to Common Prerequisite](#step-1-refer-to-common-prerequisite)
  - [Step 2: Creating Payment Parameter Object](#step-2-creating-payment-parameter-object)
  - [Step 3: Send The Quix Hosted Items Request and Retrieve Response](#step-3-send-the-quix-hosted-items-request-and-retrieve-response)
  - [Complete Example](#complete-example)
- [Quix Hosted Accommodation Request](#quix-hosted-accommodation-request)
  - [Step 1: Refer to Common Prerequisite](#step-1-refer-to-common-prerequisite-1)
  - [Step 2: Creating Payment Parameter Object](#step-2-creating-payment-parameter-object-1)
  - [Step 3: Send The Quix Accommodation Items Request and Retrieve Response](#step-3-send-the-quix-accommodation-items-request-and-retrieve-response)
  - [Complete Example](#complete-example-1)
- [Quix Hosted Service Request](#quix-hosted-service-request)
  - [Step 1: Refer to Common Prerequisite](#step-1-refer-to-common-prerequisite-2)
  - [Step 2: Creating Payment Parameter Object](#step-2-creating-payment-parameter-object-2)
  - [Step 3: Send The Quix Service Items Request and Retrieve Response](#step-3-send-the-quix-service-items-request-and-retrieve-response)
  - [Complete Example](#complete-example-2)
- [Quix Hosted Flights Request](#quix-hosted-flights-request)
  - [Step 1: Refer to Common Prerequisite](#step-1-refer-to-common-prerequisite-3)
  - [Step 2: Creating Payment Parameter Object](#step-2-creating-payment-parameter-object-3)
  - [Step 3: Send The Quix Hosted Flights Request and Retrieve Response](#step-3-send-the-quix-hosted-flights-request-and-retrieve-response)
  - [Complete Example](#complete-example-3)

## Common Prerequisite: Creating Credentials Object

First, instantiate the Credentials object with your merchant details. This includes your Merchant ID and Merchant Pass, which are essential for authenticating requests to the AddonPayments API. In this section, we set up the necessary credentials for the payment service. The credentials include the merchant ID, merchant password, environment, product ID, and API version.

### Steps

1. **Initialize Credentials Object:** Create a new instance of the Credentials class to hold the authentication and configuration details.
2. **Set Merchant ID:** Assign the merchant ID using the `set_merchant_id` method. This ID is provided by the payment service provider and identifies the merchant account.
3. **Set Merchant Password:** Assign the merchant password using the `set_merchant_pass` method. This password is provided by the payment service provider and is used for authentication.
4. **Set Environment:** Specify the environment (e.g., STAGING, PRODUCTION) using the `set_environment` method. This determines the endpoint URL for the payment requests.
5. **Set Product ID:** Assign the product ID using the `set_product_id` method. This ID identifies the specific product or service being paid for.
6. **Set API Version:** Specify the API version using the `set_api_version` method. This ensures compatibility with the payment service's API.
7. **Assign Credentials to Payment Service:** Finally, assign the configured credentials object to the `credentials` property of the payment service. This step is crucial as it links the payment service instance with the necessary authentication and configuration details, allowing it to authenticate and process payment requests.

```python
from sdk.models.credentials import Credentials
from sdk.enums.environment import Environment

credentials = Credentials()
credentials.set_merchant_id("116819")
credentials.set_merchant_pass("a193a2de8ed6140e848d5015620e8129")
credentials.set_environment(Environment.STAGING)
credentials.set_product_id("1168190001")
credentials.set_api_version(5)
payment_service.credentials = credentials
```

## Quix Hosted Items Request

### Step 1: Refer to Common Prerequisite

Before proceeding with the Hosted Request, please refer to the [Common Prerequisite: Creating Credentials section](#common-prerequisite-creating-credentials-object) at the beginning of this documentation for the initial setup of the SDK credentials. Ensure you have correctly configured your credentials as described there.

### Step 2: Creating Payment Parameter Object

In this step, we will provide the SDK with the payment parameters:

```python
from typing import List
from sdk.enums.category import Category
from sdk.enums.country_code import CountryCodeAlpha3
from sdk.enums.currency import Currency
from sdk.models.quix_models.quix_address import QuixAddress
from sdk.models.quix_models.quix_billing import QuixBilling
from sdk.models.quix_models.quix_product.quix_article_product import QuixArticleProduct
from sdk.models.quix_models.quix_product.quix_cart_product import QuixCartProduct
from sdk.models.quix_models.quix_product.quix_item_pay_sol_extended_data import QuixItemPaySolExtendedData
from sdk.models.quix_models.quix_product.quix_product_cart_item import QuixProductCartItem
from sdk.models.requests.quix_hosted.hosted_quix_item import HostedQuixItem

request = HostedQuixItem()
request.set_amount("99")
request.set_customer_id("903")
request.set_status_url("https://test.com/status")
request.set_cancel_url("https://test.com/cancel")
request.set_awaiting_url("https://test.com/await")
request.set_success_url("https://test.com/success")
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
quix_article_product.set_unit_price_with_tax(99)
quix_article_product.set_category(Category.DIGITAL)

quix_item_cart_item_product = QuixProductCartItem()
quix_item_cart_item_product.set_article(quix_article_product)
quix_item_cart_item_product.set_units(1)
quix_item_cart_item_product.set_auto_shipping(True)
quix_item_cart_item_product.set_total_price_with_tax(99)

items: List[QuixProductCartItem] = [quix_item_cart_item_product]

quix_cart_product = QuixCartProduct()
quix_cart_product.set_currency(Currency.EUR)
quix_cart_product.set_items(items)
quix_cart_product.set_total_price_with_tax('99')

quix_address = QuixAddress()
quix_address.set_city("Barcelona")
quix_address.set_country(CountryCodeAlpha3.ESP)
quix_address.set_street_address("Nombre de la vía y nº")
quix_address.set_postal_code("28003")

quix_billing = QuixBilling()
quix_billing.set_address(quix_address)
quix_billing.set_first_name("Nombre")
quix_billing.set_last_name("Apellido")

quix_item_pay_sol_extended_data = QuixItemPaySolExtendedData()
quix_item_pay_sol_extended_data.set_cart(quix_cart_product)
quix_item_pay_sol_extended_data.set_billing(quix_billing)
quix_item_pay_sol_extended_data.set_product("instalments")

request.set_pay_sol_extended_data(quix_item_pay_sol_extended_data)
```

### Step 3: Send The Quix Hosted Items Request and Retrieve Response

```python
from sdk.adapters.hosted_quix_payment_adapter import HostedQuixPaymentAdapter
from sdk.exceptions.field_exception import FieldException

try:
    # Send Payment Request
    result = HostedQuixPaymentAdapter(credentials).send_hosted_quix_item_request(request)
    print(result.get_notification().get_redirect_url())
except FieldException as field_exception:
    print(field_exception)
```

### Complete Example

Here is the complete example combining all the sections, including the Credentials setup, Payment Parameter configuration, and sending the request to retrieve the response:

```python
from typing import List
from sdk.adapters.hosted_quix_payment_adapter import HostedQuixPaymentAdapter
from sdk.enums.category import Category
from sdk.enums.country_code import CountryCodeAlpha3
from sdk.enums.currency import Currency
from sdk.enums.environment import Environment
from sdk.exceptions.field_exception import FieldException
from sdk.models.credentials import Credentials
from sdk.models.quix_models.quix_address import QuixAddress
from sdk.models.quix_models.quix_billing import QuixBilling
from sdk.models.quix_models.quix_product.quix_article_product import QuixArticleProduct
from sdk.models.quix_models.quix_product.quix_cart_product import QuixCartProduct
from sdk.models.quix_models.quix_product.quix_item_pay_sol_extended_data import QuixItemPaySolExtendedData
from sdk.models.quix_models.quix_product.quix_product_cart_item import QuixProductCartItem
from sdk.models.requests.quix_hosted.hosted_quix_item import HostedQuixItem

class Items:

    @staticmethod
    def send_quix_hosted_items():
        try:
            # Step 1 - Creating Credentials Object
            credentials = Credentials

()
            credentials.set_merchant_id("116819")
            credentials.set_merchant_pass("a193a2de8ed6140e848d5015620e8129")
            credentials.set_environment(Environment.STAGING)
            credentials.set_product_id("1168190001")
            credentials.set_api_version(5)

            # Step 2 - Configure Payment Parameters
            request = HostedQuixItem()
            request.set_amount("99")
            request.set_customer_id("903")
            request.set_status_url("https://test.com/status")
            request.set_cancel_url("https://test.com/cancel")
            request.set_awaiting_url("https://test.com/await")
            request.set_success_url("https://test.com/success")
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
            quix_article_product.set_unit_price_with_tax(99)
            quix_article_product.set_category(Category.DIGITAL)

            quix_item_cart_item_product = QuixProductCartItem()
            quix_item_cart_item_product.set_article(quix_article_product)
            quix_item_cart_item_product.set_units(1)
            quix_item_cart_item_product.set_auto_shipping(True)
            quix_item_cart_item_product.set_total_price_with_tax(99)

            items: List[QuixProductCartItem] = [quix_item_cart_item_product]

            quix_cart_product = QuixCartProduct()
            quix_cart_product.set_currency(Currency.EUR)
            quix_cart_product.set_items(items)
            quix_cart_product.set_total_price_with_tax('99')

            quix_address = QuixAddress()
            quix_address.set_city("Barcelona")
            quix_address.set_country(CountryCodeAlpha3.ESP)
            quix_address.set_street_address("Nombre de la vía y nº")
            quix_address.set_postal_code("28003")

            quix_billing = QuixBilling()
            quix_billing.set_address(quix_address)
            quix_billing.set_first_name("Nombre")
            quix_billing.set_last_name("Apellido")

            quix_item_pay_sol_extended_data = QuixItemPaySolExtendedData()
            quix_item_pay_sol_extended_data.set_cart(quix_cart_product)
            quix_item_pay_sol_extended_data.set_billing(quix_billing)
            quix_item_pay_sol_extended_data.set_product("instalments")

            request.set_pay_sol_extended_data(quix_item_pay_sol_extended_data)

            # Step 3 - Send Payment Request
            result = HostedQuixPaymentAdapter(credentials).send_hosted_quix_item_request(request)
            print(result.get_notification().get_redirect_url())
        except FieldException as field_exception:
            print(field_exception)

if __name__ == "__main__":
    Items.send_quix_hosted_items()
```

## Quix Hosted Accommodation Request

### Step 1: Refer to Common Prerequisite

Before proceeding with the Hosted Request, please refer to the [Common Prerequisite: Creating Credentials section](#common-prerequisite-creating-credentials-object) at the beginning of this documentation for the initial setup of the SDK credentials. Ensure you have correctly configured your credentials as described there.

### Step 2: Creating Payment Parameter Object

In this step, we will provide the SDK with the payment parameters:

```python
from sdk.enums.category import Category
from sdk.enums.country_code import CountryCodeAlpha3
from sdk.enums.currency import Currency
from sdk.models.quix_models.quix_address import QuixAddress
from sdk.models.quix_models.quix_billing import QuixBilling
from sdk.models.quix_models.quix_accommodation.auix_accommodation_cart_item import QuixAccommodationCartItem
from sdk.models.quix_models.quix_accommodation.quix_accommodation_pay_sol_extended_data import QuixAccommodationPaySolExtendedData
from sdk.models.quix_models.quix_accommodation.auix_article_accommodation import QuixArticleAccommodation
from sdk.models.quix_models.quix_accommodation.quix_cart_accommodation import QuixCartAccommodation
from sdk.models.requests.quix_hosted.hosted_quix_accommodation import HostedQuixAccommodation

request = HostedQuixAccommodation()
request.set_amount("99")
request.set_customer_id("903")
request.set_status_url("https://test.com/status")
request.set_cancel_url("https://test.com/cancel")
request.set_awaiting_url("https://test.com/await")
request.set_success_url("https://test.com/success")
request.set_error_url("https://test.com/error")
request.set_customer_email("test@mail.com")
request.set_customer_national_id("99999999R")
request.set_dob("01-12-1999")
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
quix_article_accommodation.set_unit_price_with_tax(99)
quix_article_accommodation.set_category(Category.DIGITAL)

quix_item_cart_item_accommodation = QuixAccommodationCartItem()
quix_item_cart_item_accommodation.set_article(quix_article_accommodation)
quix_item_cart_item_accommodation.set_units(1)
quix_item_cart_item_accommodation.set_auto_shipping(True)
quix_item_cart_item_accommodation.set_total_price_with_tax(99)

items = [quix_item_cart_item_accommodation]

quix_cart_accommodation = QuixCartAccommodation()
quix_cart_accommodation.set_currency(Currency.EUR)
quix_cart_accommodation.set_items(items)
quix_cart_accommodation.set_total_price_with_tax(99)

quix_billing = QuixBilling()
quix_billing.set_address(quix_address)
quix_billing.set_first_name("Nombre")
quix_billing.set_last_name("Apellido")

quix_accommodation_pay_sol_extended_data = QuixAccommodationPaySolExtendedData()
quix_accommodation_pay_sol_extended_data.set_cart(quix_cart_accommodation)
quix_accommodation_pay_sol_extended_data.set_billing(quix_billing)
quix_accommodation_pay_sol_extended_data.set_product("instalments")

request.set_pay_sol_extended_data(quix_accommodation_pay_sol_extended_data)
```

### Step 3: Send The Quix Accommodation Items Request and Retrieve Response

```python
from sdk.adapters.hosted_quix_payment_adapter import HostedQuixPaymentAdapter
from sdk.exceptions.field_exception import FieldException

try:
    # Send Payment Request
    result = HostedQuixPaymentAdapter(credentials).send_hosted_quix_accommodation_request(request)
    print(result.get_notification().get_redirect_url())
except FieldException as field_exception:
    print(field_exception)
```

### Complete Example

Here is the complete example combining all the sections, including the Credentials setup, Payment Parameter configuration, and sending the request to retrieve the response:

```python
import json
from typing import List
from sdk.adapters.hosted_quix_payment_adapter import HostedQuixPaymentAdapter
from sdk.enums.category import Category
from sdk.enums.country_code import CountryCodeAlpha3
from sdk.enums.currency import Currency
from sdk.enums.environment import Environment
from sdk.exceptions.field_exception import FieldException
from sdk.models.credentials import Credentials
from sdk.models.quix_models.quix_address import QuixAddress
from sdk.models.quix_models.quix_billing import QuixBilling
from sdk.models.quix_models.quix_accommodation.auix_accommodation_cart_item import QuixAccommodationCartItem
from sdk.models.quix_models.quix_accommodation.quix_accommodation_pay_sol_extended_data import QuixAccommodationPaySolExtendedData
from sdk.models.quix_models.quix_accommodation.auix_article_accommodation import QuixArticleAccommodation
from sdk.models.quix_models.quix_accommodation.quix_cart_accommodation import QuixCartAccommodation
from sdk.models.requests.quix_hosted.hosted_quix_accommodation import HostedQuixAccommodation
from sdk.utils.custom_encoder import CustomEncoder

class QuixHostedAccommodationService:

    @staticmethod
    def send_quix_hosted_accommodation_request():
        try:
            # Step 1 - Creating Credentials Object
            credentials = Credentials()
            credentials.set_merchant_id("116819")
            credentials.set_merchant_pass("a193a2de8ed6140e848d5015620e8129")
            credentials.set_environment(Environment.STAGING)
            credentials.set_product_id("1166590004")
            credentials.set_api_version(5)

            # Step 2 - Configure Payment Parameters
            request = HostedQuixAccommodation()
            request.set_amount("99")
            request.set_customer_id("903")
            request.set_status_url("https://test.com/status")
            request.set_cancel_url("https://test

.com/cancel")
            request.set_awaiting_url("https://test.com/await")
            request.set_success_url("https://test.com/success")
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
            quix_article_accommodation.set_unit_price_with_tax(99)
            quix_article_accommodation.set_category(Category.DIGITAL)

            quix_item_cart_item_accommodation = QuixAccommodationCartItem()
            quix_item_cart_item_accommodation.set_article(quix_article_accommodation)
            quix_item_cart_item_accommodation.set_units(1)
            quix_item_cart_item_accommodation.set_auto_shipping(True)
            quix_item_cart_item_accommodation.set_total_price_with_tax(99)

            items = [quix_item_cart_item_accommodation]

            quix_cart_accommodation = QuixCartAccommodation()
            quix_cart_accommodation.set_currency(Currency.EUR)
            quix_cart_accommodation.set_items(items)
            quix_cart_accommodation.set_total_price_with_tax(99)

            quix_billing = QuixBilling()
            quix_billing.set_address(quix_address)
            quix_billing.set_first_name("Nombre")
            quix_billing.set_last_name("Apellido")

            quix_accommodation_pay_sol_extended_data = QuixAccommodationPaySolExtendedData()
            quix_accommodation_pay_sol_extended_data.set_cart(quix_cart_accommodation)
            quix_accommodation_pay_sol_extended_data.set_billing(quix_billing)
            quix_accommodation_pay_sol_extended_data.set_product("instalments")

            request.set_pay_sol_extended_data(quix_accommodation_pay_sol_extended_data)

            print(json.dumps(request, cls=CustomEncoder))

            # Step 3 - Send Payment Request
            result = HostedQuixPaymentAdapter(credentials).send_hosted_quix_accommodation_request(request)
            print(result.get_notification().get_redirect_url())
        except FieldException as field_exception:
            print(field_exception)


if __name__ == "__main__":
    QuixHostedAccommodationService.send_quix_hosted_accommodation_request()
```

## Quix Hosted Service Request

### Step 1: Refer to Common Prerequisite

Before proceeding with the Hosted Request, please refer to the [Common Prerequisite: Creating Credentials section](#common-prerequisite-creating-credentials-object) at the beginning of this documentation for the initial setup of the SDK credentials. Ensure you have correctly configured your credentials as described there.

### Step 2: Creating Payment Parameter Object

In this step, we will provide the SDK with the payment parameters:

```python
from sdk.enums.category import Category
from sdk.enums.country_code import CountryCodeAlpha3
from sdk.enums.currency import Currency
from sdk.models.quix_models.quix_address import QuixAddress
from sdk.models.quix_models.quix_billing import QuixBilling
from sdk.models.quix_models.quix_service.quix_article_service import QuixArticleService
from sdk.models.quix_models.quix_service.quix_cart_service import QuixCartService
from sdk.models.quix_models.quix_service.quix_service_cart_item import QuixServiceCartItem
from sdk.models.quix_models.quix_service.quix_service_pay_sol_extended_data import QuixServicePaySolExtendedData
from sdk.models.requests.quix_hosted.hosted_quix_service import HostedQuixService

request = HostedQuixService()
request.set_amount("99")
request.set_customer_id("903")
request.set_status_url("https://test.com/status")
request.set_cancel_url("https://test.com/cancel")
request.set_awaiting_url("https://test.com/await")
request.set_success_url("https://test.com/success")
request.set_error_url("https://test.com/error")
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
quix_article_service.set_unit_price_with_tax(99)
quix_article_service.set_category(Category.DIGITAL)

quix_item_cart_item_service = QuixServiceCartItem()
quix_item_cart_item_service.set_article(quix_article_service)
quix_item_cart_item_service.set_units(1)
quix_item_cart_item_service.set_auto_shipping(True)
quix_item_cart_item_service.set_total_price_with_tax(99)

items = [quix_item_cart_item_service]

quix_cart_service = QuixCartService()
quix_cart_service.set_currency(Currency.EUR)
quix_cart_service.set_items(items)
quix_cart_service.set_total_price_with_tax('99')

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
```

### Step 3: Send The Quix Service Items Request and Retrieve Response

```python
from sdk.adapters.hosted_quix_payment_adapter import HostedQuixPaymentAdapter
from sdk.exceptions.field_exception import FieldException

try:
    # Send Payment Request
    result = HostedQuixPaymentAdapter(credentials).send_hosted_quix_service_request(request)
    print(result.get_notification().get_redirect_url())
except FieldException as field_exception:
    print(field_exception)
```

### Complete Example

Here is the complete example combining all the sections, including the Credentials setup, Payment Parameter configuration, and sending the request to retrieve the response:

```python
from sdk.adapters.hosted_quix_payment_adapter import HostedQuixPaymentAdapter
from sdk.enums.category import Category
from sdk.enums.country_code import CountryCodeAlpha3
from sdk.enums.currency import Currency
from sdk.enums.environment import Environment
from sdk.exceptions.field_exception import FieldException
from sdk.models.credentials import Credentials
from sdk.models.quix_models.quix_address import QuixAddress
from sdk.models.quix_models.quix_billing import QuixBilling
from sdk.models.quix_models.quix_service.quix_article_service import QuixArticleService
from sdk.models.quix_models.quix_service.quix_cart_service import QuixCartService
from sdk.models.quix_models.quix_service.quix_service_cart_item import QuixServiceCartItem
from sdk.models.quix_models.quix_service.quix_service_pay_sol_extended_data import QuixServicePaySolExtendedData
from sdk.models.requests.quix_hosted.hosted_quix_service import HostedQuixService

class QuixHostedService:

    @staticmethod
    def send_quix_hosted_service_request():
        try:
            # Step 1 - Creating Credentials Object
            credentials = Credentials()
            credentials.set_merchant_id("116819")
            credentials.set_merchant_pass("a193a2de8ed6140e848d5015620e8129")
            credentials.set_environment(Environment.STAGING)
            credentials.set_product_id("1166590002")
            credentials.set_api_version(5)

            # Step 2 - Configure Payment Parameters
            request = HostedQuixService()
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

            quix_article_service

 = QuixArticleService()
            quix_article_service.set_name("Nombre del servicio 2")
            quix_article_service.set_reference("4912345678903")
            quix_article_service.set_end_date("2024-12-31T23:59:59+01:00")
            quix_article_service.set_unit_price_with_tax(99)
            quix_article_service.set_category(Category.DIGITAL)

            quix_item_cart_item_service = QuixServiceCartItem()
            quix_item_cart_item_service.set_article(quix_article_service)
            quix_item_cart_item_service.set_units(1)
            quix_item_cart_item_service.set_auto_shipping(True)
            quix_item_cart_item_service.set_total_price_with_tax(99)

            items = [quix_item_cart_item_service]

            quix_cart_service = QuixCartService()
            quix_cart_service.set_currency(Currency.EUR)
            quix_cart_service.set_items(items)
            quix_cart_service.set_total_price_with_tax('99')

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

            # Step 3 - Send Payment Request
            result = HostedQuixPaymentAdapter(credentials).send_hosted_quix_service_request(request)
            print(result.get_notification().get_redirect_url())
        except FieldException as field_exception:
            print(field_exception)


if __name__ == "__main__":
    QuixHostedService.send_quix_hosted_service_request()
```

## Quix Hosted Flights Request

### Step 1: Refer to Common Prerequisite

Before proceeding with the Hosted Request, please refer to the [Common Prerequisite: Creating Credentials section](#common-prerequisite-creating-credentials-object) at the beginning of this documentation for the initial setup of the SDK credentials. Ensure you have correctly configured your credentials as described there.

### Step 2: Creating Payment Parameter Object

In this step, we will provide the SDK with the payment parameters:

```python
from sdk.enums.category import Category
from sdk.enums.country_code import CountryCodeAlpha3
from sdk.enums.currency import Currency
from sdk.models.quix_models.quix_address import QuixAddress
from sdk.models.quix_models.quix_billing import QuixBilling
from sdk.models.quix_models.quix_flight.quix_article_flight import QuixArticleFlight
from sdk.models.quix_models.quix_flight.auix_cart_flight import QuixCartFlight
from sdk.models.quix_models.quix_flight.auix_flight_cart_item import QuixFlightCartItem
from sdk.models.quix_models.quix_flight.quix_flight_pay_sol_extended_data import QuixFlightPaySolExtendedData
from sdk.models.quix_models.quix_flight.quix_passenger_flight import QuixPassengerFlight
from sdk.models.quix_models.quix_flight.quix_segment_flight import QuixSegmentFlight
from sdk.models.requests.quix_hosted.hosted_quix_flight import HostedQuixFlight

request = HostedQuixFlight()
request.set_amount("99")
request.set_customer_id("903")
request.set_status_url("https://test.com/status")
request.set_cancel_url("https://test.com/cancel")
request.set_awaiting_url("https://test.com/await")
request.set_success_url("https://test.com/success")
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
```

### Step 3: Send The Quix Hosted Flights Request and Retrieve Response

```python
from sdk.adapters.hosted_quix_payment_adapter import HostedQuixPaymentAdapter
from sdk.exceptions.field_exception import FieldException

try:
    # Send Payment Request
    result = HostedQuixPaymentAdapter(credentials).send_hosted_quix_flight_request(request)
    print(result.get_notification().get_redirect_url())
except FieldException as field_exception:
    print(field_exception)
```

### Complete Example

Here is the complete example combining all the sections, including the Credentials setup, Payment Parameter configuration, and sending the request to retrieve the response:

```python
from sdk.adapters.hosted_quix_payment_adapter import HostedQuixPaymentAdapter
from sdk.enums.category import Category
from sdk.enums.country_code import CountryCodeAlpha3
from sdk.enums.currency import Currency
from sdk.enums.environment import Environment
from sdk.exceptions.field_exception import FieldException
from sdk.models.credentials import Credentials
from sdk.models.quix_models.quix_address import QuixAddress
from sdk.models.quix_models.quix_billing import QuixBilling
from sdk.models.quix_models.quix_flight.quix_article_flight import QuixArticleFlight
from sdk.models.quix_models.quix_flight.auix_cart_flight import QuixCartFlight
from sdk.models.quix_models.quix_flight.auix_flight_cart_item import QuixFlightCartItem
from sdk.models.quix_models.quix_flight.quix_flight_pay_sol_extended_data import QuixFlightPaySolExtendedData
from sdk.models.quix_models.quix_flight.quix_passenger_flight import QuixPassengerFlight
from sdk.models.quix_models.quix_flight.quix_segment_flight import QuixSegmentFlight
from sdk.models.requests.quix_hosted.hosted_quix_flight import HostedQuixFlight

class QuixHostedFlightService:

    @staticmethod
    def send_quix_hosted_flights_request():
        try:
            # Step 1 - Creating Credentials Object
            credentials = Credentials()
            credentials.set_merchant_id("116819")
            credentials.set_merchant_pass("a193a2de8ed6140e848d5015620e8129")
            credentials.set_environment(Environment.STAGING)
            credentials.set_product_id("1166590003")
            credentials.set_api_version(5)

            # Step 2 - Configure Payment Parameters
            request = HostedQuixFlight()
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
            request.set_first_name

("Name")
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

            # Step 3 - Send Payment Request
            result = HostedQuixPaymentAdapter(credentials).send_hosted_quix_flight_request(request)
            print(result.get_notification().get_redirect_url())

        except FieldException as field_exception:
            print(field_exception)


if __name__ == "__main__":
    QuixHostedFlightService.send_quix_hosted_flights_request()
```