# Hosted

This documentation focuses on how to make Hosted transactions using the SDK. This payment method involves sending the payment details and then displaying a web page directed from the AddonPayments for the user to enter the card data and proceed with the transaction.

## Table of Contents

- [Common Prerequisite: Creating Credentials Object](#common-prerequisite-creating-credentials-object)
  - [Steps](#steps)
- [Hosted Request](#hosted-request)
  - [Step 1: Refer to Common Prerequisite](#step-1-refer-to-common-prerequisite)
  - [Step 2: Creating Payment Parameter Object](#step-2-creating-payment-parameter-object)
  - [Step 3: Send The Hosted Request and Retrieve Response](#step-3-send-the-hosted-request-and-retrieve-response)
- [Hosted Recurring](#hosted-recurring)
  - [Step 1: Refer to Common Prerequisite](#step-1-refer-to-common-prerequisite)
  - [Step 2: Creating Payment Parameter Object](#step-2-creating-payment-parameter-object)
  - [Step 3: Send The Hosted Recurring Request and Retrieve Response](#step-3-send-the-hosted-recurring-request-and-retrieve-response)
- [Complete Example](#complete-example)

## Common Prerequisite: Creating Credentials Object

First, instantiate the `Credentials` object with your merchant details. This includes your Merchant ID, Merchant Pass which are essential for authenticating requests to the AddonPayments API. In this section, we set up the necessary credentials for the payment service. The credentials include the merchant ID, merchant password, environment, product ID, and API version.

### Steps

1. **Initialize Credentials Object:** Create a new instance of the `Credentials` class to hold the authentication and configuration details.
2. **Set Merchant ID:** Assign the merchant ID using the `set_merchant_id` method. This ID is provided by the payment service provider and identifies the merchant account.
3. **Set Merchant Password:** Assign the merchant password using the `set_merchant_pass` method. This password is provided by the payment service provider and is used for authentication.
4. **Set Environment:** Specify the environment (e.g., STAGING, PRODUCTION) using the `set_environment` method. This determines the endpoint URL for the payment requests.
5. **Set Product ID:** Assign the product ID using the `set_product_id` method. This ID identifies the specific product or service being paid for.
6. **Set API Version:** Specify the API version using the `set_api_version` method. This ensures compatibility with the payment service's API.
7. **Assign Credentials to Payment Service:** Finally, assign the configured credentials object to the credentials property of the payment service. This step is crucial as it links the payment service instance with the necessary authentication and configuration details, allowing it to authenticate and process payment requests.

```python
from sdk.models.credentials import Credentials
from sdk.enums.environment import Environment

credentials = Credentials()
credentials.set_merchant_id("your_merchant_id")
credentials.set_merchant_pass("your_merchant_pass")
credentials.set_environment(Environment.STAGING)
credentials.set_product_id("your_product_id")
credentials.set_api_version(5)
```

## Hosted Request

Sending a normal payment request which is used in a normal payment scenario.

### Step 1: Refer to Common Prerequisite

Before proceeding with the Hosted Request, please refer to the [Common Prerequisite: Creating Credentials section](#common-prerequisite-creating-credentials-object) at the beginning of this documentation for the initial setup of the SDK credentials. Ensure you have correctly configured your credentials as described there.

### Step 2: Creating Payment Parameter Object

In this step, we will provide the SDK with the payment parameters:

- Amount
- Currency
- Country
- Customer Id
- Merchant Transaction Id
- Payment Solution
- Status URL
- Error URL
- Success URL
- Cancel URL
- Awaiting URL

```python
from sdk.enums.country_code import CountryCodeAlpha2
from sdk.enums.currency import Currency
from sdk.enums.payment_solutions import PaymentSolutions
from sdk.models.requests.hosted.hosted_payment_redirection import HostedPaymentRedirection

request = HostedPaymentRedirection()
request.set_amount("50")
request.set_currency(Currency.EUR)
request.set_country(CountryCodeAlpha2.ES)
request.set_customer_id("903")
request.set_merchant_transaction_id("3123123")
request.set_payment_solution(PaymentSolutions.creditcards)
request.set_status_url("https://test.com/status")
request.set_success_url("https://test.com/success")
request.set_error_url("https://test.com/error")
request.set_awaiting_url("https://test.com/awaiting")
request.set_cancel_url("https://test.com/cancel")
request.set_force_token_request(False)
```

### Step 3: Send The Hosted Request and Retrieve Response

The response from the payment service can be handled using a custom response handler. Below is a code snippet showing how to send the hosted payment request and retrieve the redirection URL.

```python
from sdk.adapters.hosted_payment_adapter import HostedPaymentAdapter
from sdk.exceptions.field_exception import FieldException

try:
    result = HostedPaymentAdapter(credentials).send_hosted_payment_request(request)
    print(result.get_redirect_url())
except FieldException as field_exception:
    print(field_exception)
```

Note: It's important to note that the status of the transaction, whether it's a success or an error, will be communicated asynchronously via a webhook notification. Within the SDK, we've included a method to create a webhook and notification handler, enabling you to receive these transaction notifications efficiently and take action. This allows for real-time updates on transaction statuses directly within your application.

## Hosted Recurring

Sending a normal payment request which is used in a recurring payment scenario.

### Step 1: Refer to Common Prerequisite

Before proceeding with the Hosted Recurring Request, please refer to the [Common Prerequisite: Creating Credentials section](#common-prerequisite-creating-credentials-object) at the beginning of this documentation for the initial setup of the SDK credentials. Ensure you have correctly configured your credentials as described there.

### Step 2: Creating Payment Parameter Object

In this step, we will provide the SDK with the payment parameters:

- Amount
- Currency
- Country
- Customer Id
- Payment Recurring Type
- Challenge Ind
- Merchant Transaction Id
- Payment Solution
- Status URL
- Error URL
- Success URL
- Cancel URL
- Awaiting URL

```python
from sdk.enums.country_code import CountryCodeAlpha2
from sdk.enums.currency import Currency
from sdk.enums.payment_recurring_type import PaymentRecurringType
from sdk.enums.payment_solutions import PaymentSolutions
from sdk.models.requests.hosted.hosted_payment_recurrent_initial import HostedPaymentRecurrentInitial

request = HostedPaymentRecurrentInitial()
request.set_amount("50")
request.set_currency(Currency.EUR)
request.set_country(CountryCodeAlpha2.ES)
request.set_customer_id("903")
request.set_payment_recurring_type(PaymentRecurringType.newCof)
request.set_merchant_transaction_id("3123123")
request.set_payment_solution(PaymentSolutions.creditcards)
request.set_status_url("https://test.com/status")
request.set_success_url("https://test.com/success")
request.set_error_url("https://test.com/error")
request.set_awaiting_url("https://test.com/awaiting")
request.set_cancel_url("https://test.com/cancel")
request.set_force_token_request(False)
```

### Step 3: Send The Hosted Recurring Request and Retrieve Response

The response from the payment service can be handled using a custom response handler. Below is a code snippet showing how to send the hosted recurring payment request and retrieve the redirection URL.

```python
from sdk.adapters.hosted_payment_adapter import HostedPaymentAdapter
from sdk.exceptions.field_exception import FieldException

try:
    result = HostedPaymentAdapter(credentials).send_hosted_payment_recurrent_initial(request)
    print(result.get_redirect_url())
except FieldException as field_exception:
    print(field_exception)
```

Note: It's important to note that the status of the transaction, whether it's a success or an error, will be communicated asynchronously via a webhook notification. Within the SDK, we've included a method to create a webhook and notification handler, enabling you to receive these transaction notifications efficiently and take action. This allows for real-time updates on transaction statuses directly within your application.

## Complete Example

Here is the complete example combining all the sections, including the creation of credentials, configuration of payment parameters, and sending the payment request.

```python
from sdk.adapters.hosted_payment_adapter import HostedPaymentAdapter
from sdk.enums.country_code import CountryCodeAlpha2
from sdk.enums.currency import Currency
from sdk.enums.environment import Environment
from sdk.enums.payment_solutions import PaymentSolutions
from sdk.exceptions.field_exception import FieldException
from sdk.models.credentials import Credentials
from sdk.models.requests.hosted.hosted_payment_redirection import HostedPaymentRedirection

class Hosted:

    @staticmethod
    def send_hosted_payment_request():
        try:
            # Step 1 - Creating Credentials Object
            credentials = Credentials()
            credentials.set_merchant_id("your_merchant_id")
            credentials.set_merchant_pass("your_merchant_pass")
            credentials.set_environment(Environment.STAGING)
            credentials.set_product_id("your_product_id")
            credentials.set_api_version(5)

            # Step 2 - Configure Payment Parameters
            request = HostedPaymentRedirection()
            request.set_amount("50")
            request.set_currency(Currency.EUR)
            request.set_country(CountryCodeAlpha2.ES)
            request.set_customer_id("903")
            request.set_merchant_transaction_id("3123123")
            request.set_payment_solution(PaymentSolutions.creditcards)
            request.set_status_url("https://test.com/status")


            request.set_success_url("https://test.com/success")
            request.set_error_url("https://test.com/error")
            request.set_awaiting_url("https://test.com/awaiting")
            request.set_cancel_url("https://test.com/cancel")
            request.set_force_token_request(False)

            # Step 3 - Send Payment Request
            result = HostedPaymentAdapter(credentials).send_hosted_payment_request(request)
            print(result.get_redirect_url())
        except FieldException as field_exception:
            print(field_exception)

if __name__ == "__main__":
    Hosted.send_hosted_payment_request()
```

This completes the quick start guide for using the Python SDK to handle Hosted transactions. Follow the steps carefully to ensure successful implementation.