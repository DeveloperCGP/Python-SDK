# JavaScript

## Table of Contents

- [Common Prerequisite: Creating Credentials Object](#common-prerequisite-creating-credentials-object)
  - [Steps](#steps)
- [Use Case 1: JavaScript Authentication Request](#use-case-1-javascript-authentication-request)
  - [Step 1: Refer to Common Prerequisite](#step-1-refer-to-common-prerequisite)
  - [Step 2: Setting Payment Parameters](#step-2-setting-payment-parameters)
  - [Step 3: Sending the Authentication Request and Retrieve it](#step-3-sending-the-authentication-request-and-retrieve-it)
  - [Full Example](#full-example)
- [Use Case 2: JavaScript Charge Request](#use-case-2-javascript-charge-request)
  - [Step 1: Refer to Common Prerequisite](#step-1-refer-to-common-prerequisite-1)
  - [Step 2: Setting Payment Parameters for Charge Request](#step-2-setting-payment-parameters-for-charge-request)
  - [Step 3: Sending the Charge Request and Retrieve it](#step-3-sending-the-charge-request-and-retrieve-it)
  - [Full Example](#full-example-1)
- [Use Case 3: JavaScript Charge Recurring Request](#use-case-3-javascript-charge-recurring-request)
  - [Step 1: Refer to Common Prerequisite](#step-1-refer-to-common-prerequisite-2)
  - [Step 2: Setting Payment Parameters for Charge Request](#step-2-setting-payment-parameters-for-charge-request-1)
  - [Step 3: Sending the Charge Request and Retrieve it](#step-3-sending-the-charge-request-and-retrieve-it-1)
  - [Full Example](#full-example-2)

## Common Prerequisite: Creating Credentials Object

First, instantiate the Credentials object with your merchant details. This includes your Merchant ID and Merchant Pass, which are essential for authenticating requests to the AddonPayments API. In this section, we set up the necessary credentials for the payment service. The credentials include the merchant ID, merchant password, environment, product ID, and API version.

### Steps

1. **Initialize Credentials Object:** Create a new instance of the Credentials class to hold the authentication and configuration details.
2. **Set Merchant ID:** Assign the merchant ID using the `set_merchant_id` method. This ID is provided by the payment service provider and identifies the merchant account.
3. **Set Merchant Key:** Assign the merchant key using the `set_merchant_key` method. This key is provided by the payment service provider and is used for authentication.
4. **Set Environment:** Specify the environment (e.g., STAGING, PRODUCTION) using the `set_environment` method. This determines the endpoint URL for the payment requests.
5. **Set Product ID:** Assign the product ID using the `set_product_id` method. This ID identifies the specific product or service being paid for.
6. **Set API Version:** Specify the API version using the `set_api_version` method. This ensures compatibility with the payment service's API.
7. **Assign Credentials to Payment Service:** Finally, assign the configured credentials object to the credentials property of the payment service. This step is crucial as it links the payment service instance with the necessary authentication and configuration details, allowing it to authenticate and process payment requests.

```python
from sdk.models.credentials import Credentials
from sdk.enums.environment import Environment

credentials = Credentials()
credentials.set_merchant_id("116819")
credentials.set_merchant_pass("a193a2de8ed6140e848d5015620e8129")
credentials.set_environment(Environment.STAGING)
credentials.set_product_id("1168190001")
credentials.set_api_version(5)
credentials.set_merchant_key("3535457e-qe21-40t7-863e-e5838e53499e")
payment_service.credentials = credentials
```

## Use Case 1: JavaScript Authentication Request

### Step 1: Refer to Common Prerequisite

Before proceeding with the Hosted Request, please refer to the [Common Prerequisite: Creating Credentials section](#common-prerequisite-creating-credentials-object) at the beginning of this documentation for the initial setup of the SDK credentials. Ensure you have correctly configured your credentials as described there.

### Step 2: Setting Payment Parameters

In this step, we will provide the SDK with the payment parameters:

- Amount
- Currency
- Country
- Customer Id

```python
from sdk.models.requests.js.JSAuthorizationRequest import JSAuthorizationRequest
from sdk.enums.country_code import CountryCodeAlpha2
from sdk.enums.currency import Currency
from sdk.enums.operation_types import OperationTypes

request = JSAuthorizationRequest()
request.set_customer_id("8881")
request.set_currency(Currency.EUR)
request.set_country(CountryCodeAlpha2.ES)
request.set_operation_type(OperationTypes.DEBIT)
```

### Step 3: Sending the Authentication Request and Retrieve it

```python
from sdk.adapters.js_payment_adapter import JSPaymentAdapter
from sdk.exceptions.field_exception import FieldException

try:
   # Step 3 - Send Payment Request
   result = JSPaymentAdapter(credentials).send_js_authorization_request(request)
   print(result.get_auth_token())
except FieldException as field_exception:
   print(field_exception)
```

### Full Example

```python
from sdk.adapters.js_payment_adapter import JSPaymentAdapter
from sdk.enums.country_code import CountryCodeAlpha2
from sdk.enums.currency import Currency
from sdk.enums.environment import Environment
from sdk.enums.operation_types import OperationTypes
from sdk.exceptions.field_exception import FieldException
from sdk.models.credentials import Credentials
from sdk.models.requests.js.JSAuthorizationRequest import JSAuthorizationRequest

class Auth:

    @staticmethod
    def send_auth_payment_request():
        try:
            # Step 1 - Creating Credentials Object
            credentials = Credentials()
            credentials.set_merchant_id("116819")
            credentials.set_merchant_pass("a193a2de8ed6140e848d5015620e8129")
            credentials.set_environment(Environment.STAGING)
            credentials.set_merchant_key("34551e2e-qe21-40e7-863e-e54a0e53477c")
            credentials.set_product_id("1168190001")
            credentials.set_api_version(5)

            # Step 2 - Configure Payment Parameters
            request = JSAuthorizationRequest()
            request.set_country(CountryCodeAlpha2.ES)
            request.set_customer_id("55")
            request.set_currency(Currency.EUR)
            request.set_operation_type(OperationTypes.DEBIT)
            request.set_anonymous_customer(False)

            # Step 3 - Send Payment Request
            result = JSPaymentAdapter(credentials).send_js_authorization_request(request)
            print(result.get_auth_token())
        except FieldException as field_exception:
            print(field_exception)

if __name__ == "__main__":
    Auth.send_auth_payment_request()
```

## Use Case 2: JavaScript Charge Request

### Step 1: Refer to Common Prerequisite

Before proceeding with the Hosted Request, please refer to the [Common Prerequisite: Creating Credentials section](#common-prerequisite-creating-credentials-object) at the beginning of this documentation for the initial setup of the SDK credentials. Ensure you have correctly configured your credentials as described there.

### Step 2: Setting Payment Parameters for Charge Request

In this step, we will provide the SDK with the payment parameters:

- Amount
- Currency
- Country
- Customer Id
- Merchant Transaction Id
- Payment Solution
- Operation Type
- Prepay Token
- StatusURL
- ErrorURL
- SuccessURL
- CancelURL
- AwaitingURL

```python
from sdk.models.requests.js.js_charge import JSCharge
from sdk.enums.country_code import CountryCodeAlpha2
from sdk.enums.currency import Currency
from sdk.enums.operation_types import OperationTypes
from sdk.enums.payment_solutions import PaymentSolutions

request = JSCharge()
request.set_amount("50")
request.set_customer_id("8881")
request.set_currency(Currency.EUR)
request.set_country(CountryCodeAlpha2.ES)
request.set_operation_type(OperationTypes.DEBIT)
request.set_payment_solution(PaymentSolutions.creditcards)
request.set_merchant_transaction_id("55555555")
request.set_prepay_token("45357b66-8f04-4276-84f4-d35c885bde8e")
request.set_status_url("https://test.com/status")
request.set_success_url("https://test.com/success")
request.set_error_url("https://test.com/fail")
request.set_awaiting_url("https://test.com/await")
request.set_cancel_url("https://test.com/cancel")
```

### Step 3: Sending the Charge Request and Retrieve it

```python
from sdk.adapters.js_payment_adapter import JSPaymentAdapter
from sdk.exceptions.field_exception import FieldException

try:        
    result = JSPaymentAdapter(credentials).send_js_charge_request(request)
    print(result.get_notification().get_redirect_url())
except FieldException as field_exception:
    print(field_exception)
```

### Full Example

```python
from sdk.adapters.js_payment_adapter import JSPaymentAdapter
from sdk.enums.country_code import CountryCodeAlpha2
from sdk.enums.currency import Currency
from sdk.enums.environment import Environment
from sdk.enums.operation_types import OperationTypes
from sdk.enums.payment_solutions import PaymentSolutions
from sdk.exceptions.field_exception import FieldException
from sdk.models.credentials import Credentials
from sdk.models.requests.js.js_charge import JSCharge

class Charge:

    @staticmethod
    def send_charge_payment_request():
        try:
            # Step 1 - Creating Credentials Object
            credentials = Credentials()
            credentials.set_merchant_id("116819

")
            credentials.set_merchant_pass("a193a2de8ed6140e848d5015620e8129")
            credentials.set_environment(Environment.STAGING)
            credentials.set_merchant_key("34551e2e-qe21-40e7-863e-e54a0e53477c")
            credentials.set_product_id("1168190001")
            credentials.set_api_version(5)

            # Step 2 - Configure Payment Parameters
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

            merchant_params = [
                ("name", "pablo"),
                ("surname", "ferrer")
            ]

            request.set_merchant_params(merchant_params)

            # Step 3 - Send Payment Request
            result = JSPaymentAdapter(credentials).send_js_charge_request(request)
            print(result.get_notification().get_redirect_url())
        except FieldException as field_exception:
            print(field_exception)

if __name__ == "__main__":
    Charge.send_charge_payment_request()
```

## Use Case 3: JavaScript Charge Recurring Request

### Step 1: Refer to Common Prerequisite

Before proceeding with the Hosted Request, please refer to the [Common Prerequisite: Creating Credentials section](#common-prerequisite-creating-credentials-object) at the beginning of this documentation for the initial setup of the SDK credentials. Ensure you have correctly configured your credentials as described there.

### Step 2: Setting Payment Parameters for Charge Request

In this step, we will provide the SDK with the payment parameters:

- Amount
- Currency
- Country
- Customer Id
- Merchant Transaction Id
- Payment Solution
- Operation Type
- Prepay Token
- StatusURL
- ErrorURL
- SuccessURL
- CancelURL
- AwaitingURL

```python
from sdk.models.requests.js.js_payment_recurrent_initial import JSPaymentRecurrentInitial
from sdk.enums.country_code import CountryCodeAlpha2
from sdk.enums.currency import Currency
from sdk.enums.operation_types import OperationTypes
from sdk.enums.payment_recurring_type import PaymentRecurringType
from sdk.enums.payment_solutions import PaymentSolutions

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
```

### Step 3: Sending the Charge Request and Retrieve it

```python
from sdk.adapters.js_payment_adapter import JSPaymentAdapter
from sdk.exceptions.field_exception import FieldException

try:        
    result = JSPaymentAdapter(credentials).send_js_payment_recurrent_initial(request)
    print(result.get_notification().get_redirect_url())
except FieldException as field_exception:
    print(field_exception)
```

### Full Example

```python
from sdk.adapters.js_payment_adapter import JSPaymentAdapter
from sdk.enums.country_code import CountryCodeAlpha2
from sdk.enums.currency import Currency
from sdk.enums.environment import Environment
from sdk.enums.operation_types import OperationTypes
from sdk.enums.payment_recurring_type import PaymentRecurringType
from sdk.enums.payment_solutions import PaymentSolutions
from sdk.exceptions.field_exception import FieldException
from sdk.models.credentials import Credentials
from sdk.models.requests.js.js_payment_recurrent_initial import JSPaymentRecurrentInitial

class ChargeRecurring:

    @staticmethod
    def send_charge_recurring_payment_request():
        try:
            # Step 1 - Creating Credentials Object
            credentials = Credentials()
            credentials.set_merchant_id("116819")
            credentials.set_merchant_pass("a193a2de8ed6140e848d5015620e8129")
            credentials.set_environment(Environment.STAGING)
            credentials.set_merchant_key("34551e2e-qe21-40e7-863e-e54a0e53477c")
            credentials.set_product_id("1168190001")
            credentials.set_api_version(5)

            # Step 2 - Configure Payment Parameters
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

            # Step 3 - Send Payment Request
            result = JSPaymentAdapter(credentials).send_js_payment_recurrent_initial(request)
            print(result.get_notification().get_redirect_url())
        except FieldException as field_exception:
            print(field_exception)

if __name__ == "__main__":
    ChargeRecurring.send_charge_recurring_payment_request()
```