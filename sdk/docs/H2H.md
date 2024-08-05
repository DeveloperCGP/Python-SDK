# H2H

This Page provides a step-by-step guide for implementing Host-to-Host payment transactions using the Python SDK. This method enables direct communication between the merchant's server and the AddonPayments API, offering a more integrated and seamless payment processing experience.

## Table of Contents

- [Common Prerequisite: Creating Credentials Object](#common-prerequisite-creating-credentials-object)
  - [Steps](#steps)
- [H2H Request](#h2h-request)
  - [Step 1: Refer to Common Prerequisite](#step-1-refer-to-common-prerequisite)
  - [Step 2: Creating Payment Parameter Object](#step-2-creating-payment-parameter-object)
  - [Step 3: Send The H2H Request and Retrieve Response](#step-3-send-the-h2h-request-and-retrieve-response)
- [Pre-Authorization Request](#pre-authorization-request)
  - [Step 1: Refer to Common Prerequisite](#step-1-refer-to-common-prerequisite)
  - [Step 2: Creating Payment Parameter Object](#step-2-creating-payment-parameter-object)
  - [Step 3: Send The Pre-Authorization Request and Retrieve Response](#step-3-send-the-pre-authorization-request-and-retrieve-response)
- [Capture Pre-Authorization](#capture-pre-authorization)
  - [Step 1: Refer to Common Prerequisite](#step-1-refer-to-common-prerequisite)
  - [Step 2: Creating Payment Parameter Object](#step-2-creating-payment-parameter-object)
  - [Step 3: Send The H2H Capture Request and Retrieve Response](#step-3-send-the-h2h-capture-request-and-retrieve-response)
- [Void Pre-Authorization](#void-pre-authorization)
  - [Step 1: Refer to Common Prerequisite](#step-1-refer-to-common-prerequisite)
  - [Step 2: Creating Payment Parameter Object](#step-2-creating-payment-parameter-object)
  - [Step 3: Send The H2H Void Request and Retrieve Response](#step-3-send-the-h2h-void-request-and-retrieve-response)
- [Recurrent Initial](#recurrent-initial)
  - [Step 1: Refer to Common Prerequisite](#step-1-refer-to-common-prerequisite)
  - [Step 2: Creating Payment Parameter Object](#step-2-creating-payment-parameter-object)
  - [Step 3: Send The H2H Recurrent Initial Request and Retrieve Response](#step-3-send-the-h2h-recurrent-initial-request-and-retrieve-response)
- [Recurrent Subsequent](#recurrent-subsequent)
  - [Step 1: Refer to Common Prerequisite](#step-1-refer-to-common-prerequisite)
  - [Step 2: Creating Payment Parameter Object](#step-2-creating-payment-parameter-object)
  - [Step 3: Send The H2H Recurrent Subsequent Request and Retrieve Response](#step-3-send-the-h2h-recurrent-subsequent-request-and-retrieve-response)
- [Refund](#refund)
  - [Step 1: Refer to Common Prerequisite](#step-1-refer-to-common-prerequisite)
  - [Step 2: Creating Payment Parameter Object](#step-2-creating-payment-parameter-object)
  - [Step 3: Send The H2H Refund Request and Retrieve Response](#step-3-send-the-h2h-refund-request-and-retrieve-response)

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

## H2H Request

Sending a normal H2H payment request which is used in a typical payment scenario.

### Step 1: Refer to Common Prerequisite

Before proceeding with the H2H Request, please refer to the [Common Prerequisite: Creating Credentials section](#common-prerequisite-creating-credentials-object) at the beginning of this documentation for the initial setup of the SDK credentials. Ensure you have correctly configured your credentials as described there.

### Step 2: Creating Payment Parameter Object

In this step, we will provide the SDK with the payment parameters:

- Amount
- Currency
- Country
- Customer Id
- Merchant Transaction Id
- Payment Solution
- ChName
- CardNumber
- ExpDate
- CvnNumber
- Status URL
- Error URL
- Success URL
- Cancel URL
- Awaiting URL

```python
from sdk.models.requests.h2h.h2h_redirection import H2HRedirection
from sdk.enums.currency import Currency
from sdk.enums.country_code import CountryCodeAlpha2
from sdk.enums.payment_solutions import PaymentSolutions

request = H2HRedirection()
request.set_amount("50")
request.set_currency(Currency.EUR)
request.set_country(CountryCodeAlpha2.ES)
request.set_customer_id("903")
request.set_card_number("4907270002222227")
request.set_merchant_transaction_id("4556115")
request.set_ch_name("Pablo")
request.set_cvn_number("123")
request.set_exp_date("0230")
request.set_payment_solution(PaymentSolutions.creditcards)
request.set_status_url("https://test.com/status")
request.set_success_url("https://test.com/success")
request.set_error_url("https://test.com/error")
request.set_awaiting_url("https://test.com/awaiting")
request.set_cancel_url("https://test.com/cancel")
request.set_force_token_request(False)
```

### Step 3: Send The H2H Request and Retrieve Response

The response from the payment service can be handled using a custom response handler. Below is a code snippet showing how to send the H2H payment request and retrieve the redirection URL.

```python
from sdk.adapters.h2h_payment_adapter import H2HPaymentAdapter
from sdk.exceptions.field_exception import FieldException

try:
    result = H2HPaymentAdapter(credentials).send_h2h_payment_request(request)
    print(result.get_notification().get_redirect_url())
except FieldException as field_exception:
    print(field_exception)
```

### Complete Example

Here is the complete example combining all the sections, including the creation of credentials, configuration of payment parameters, and sending the payment request.

```python
from sdk.adapters.h2h_payment_adapter import H2HPaymentAdapter
from sdk.enums.country_code import CountryCodeAlpha2
from sdk.enums.currency import Currency
from sdk.enums.environment import Environment
from sdk.enums.payment_solutions import PaymentSolutions
from sdk.exceptions.field_exception import FieldException
from sdk.models.credentials import Credentials
from sdk.models.requests.h2h.h2h_redirection import H2HRedirection

class H2H:

    @staticmethod
    def send_h2h_payment_request():
        try:
            # Step 1 - Creating Credentials Object
            credentials = Credentials()
            credentials.set_merchant_id("your_merchant_id")
            credentials.set_merchant_pass("your_merchant_pass")
            credentials.set_environment(Environment.STAGING)
            credentials.set_product_id("your_product_id")
            credentials.set_api_version(5)

            # Step 2 - Configure Payment Parameters
            request = H2HRedirection()
            request.set_amount("50")
            request.set_currency(Currency.EUR)
            request.set_country(CountryCodeAlpha2.ES)
            request.set_card_number("4907270002222227")
            request.set_customer_id("903")
            request.set_ch_name("Pablo")
            request.set_cvn_number("123")
            request.set_exp_date("0230")
            request.set_payment_solution(PaymentSolutions.creditcards)
            request.set_status_url("https://test.com/status")
            request.set_success_url("https://test.com/success")
            request.set_error_url("https://test.com/error")
            request.set_awaiting_url

("https://test.com/awaiting")
            request.set_cancel_url("https://test.com/cancel")
            request.set_force_token_request(False)

            merchant_params = [
                ("name", "pablo"),
                ("surname", "ferrer")
            ]

            request.set_merchant_params(merchant_params)

            # Step 3 - Send Payment Request
            result = H2HPaymentAdapter(credentials).send_h2h_payment_request(request)
            print(result.get_notification().get_redirect_url())
        except FieldException as field_exception:
            print(field_exception)

if __name__ == "__main__":
    H2H.send_h2h_payment_request()
```

Note: It's important to note that the status of the transaction, whether it's a success or an error, will be communicated asynchronously via a webhook notification. Within the SDK, we've included a method to create a webhook and notification handler, enabling you to receive these transaction notifications efficiently and take action. This allows for real-time updates on transaction statuses directly within your application.

## Pre-Authorization Request

Sending a normal Pre-Authorization H2H request.

### Step 1: Refer to Common Prerequisite

Before proceeding with the Pre-Authorization Request, please refer to the [Common Prerequisite: Creating Credentials section](#common-prerequisite-creating-credentials-object) at the beginning of this documentation for the initial setup of the SDK credentials. Ensure you have correctly configured your credentials as described there.

### Step 2: Creating Payment Parameter Object

In this step, we will provide the SDK with the payment parameters:

- Amount
- Currency
- Country
- Customer Id
- Merchant Transaction Id
- Payment Solution
- ChName
- CardNumber
- ExpDate
- CvnNumber
- Status URL
- Error URL
- Success URL
- Cancel URL
- Awaiting URL

```python
from sdk.models.requests.h2h.h2h_pre_authorization import H2HPreAuthorization
from sdk.enums.currency import Currency
from sdk.enums.country_code import CountryCodeAlpha2
from sdk.enums.payment_solutions import PaymentSolutions

request = H2HPreAuthorization()
request.set_amount("50")
request.set_currency(Currency.EUR)
request.set_country(CountryCodeAlpha2.ES)
request.set_customer_id("903")
request.set_card_number("4907270002222227")
request.set_merchant_transaction_id("4556115")
request.set_ch_name("Pablo")
request.set_cvn_number("123")
request.set_exp_date("0230")
request.set_payment_solution(PaymentSolutions.creditcards)
request.set_status_url("https://test.com/status")
request.set_success_url("https://test.com/success")
request.set_error_url("https://test.com/error")
request.set_awaiting_url("https://test.com/awaiting")
request.set_cancel_url("https://test.com/cancel")
```

### Step 3: Send The Pre-Authorization Request and Retrieve Response

The response from the payment service can be handled using a custom response handler. Below is a code snippet showing how to send the Pre-Authorization payment request and retrieve the redirection URL.

```python
from sdk.adapters.h2h_payment_adapter import H2HPaymentAdapter
from sdk.exceptions.field_exception import FieldException

try:
    result = H2HPaymentAdapter(credentials).send_h2h_pre_authorization_request(request)
    print(result.get_notification().get_redirect_url())
except FieldException as field_exception:
    print(field_exception)
```

### Complete Example

Here is the complete example combining all the sections, including the creation of credentials, configuration of payment parameters, and sending the payment request.

```python
from sdk.adapters.h2h_payment_adapter import H2HPaymentAdapter
from sdk.enums.country_code import CountryCodeAlpha2
from sdk.enums.currency import Currency
from sdk.enums.environment import Environment
from sdk.enums.payment_solutions import PaymentSolutions
from sdk.exceptions.field_exception import FieldException
from sdk.models.credentials import Credentials
from sdk.models.requests.h2h.h2h_pre_authorization import H2HPreAuthorization

class PreAuthorization:

    @staticmethod
    def send_pre_authorization_payment_request():
        try:
            # Step 1 - Creating Credentials Object
            credentials = Credentials()
            credentials.set_merchant_id("your_merchant_id")
            credentials.set_merchant_pass("your_merchant_pass")
            credentials.set_environment(Environment.STAGING)
            credentials.set_product_id("your_product_id")
            credentials.set_api_version(5)

            # Step 2 - Configure Payment Parameters
            request = H2HPreAuthorization()
            request.set_amount("50")
            request.set_currency(Currency.EUR)
            request.set_country(CountryCodeAlpha2.ES)
            request.set_customer_id("903")
            request.set_card_number("4907270002222227")
            request.set_ch_name("Pablo")
            request.set_cvn_number("123")
            request.set_exp_date("0230")
            request.set_payment_solution(PaymentSolutions.creditcards)
            request.set_status_url("https://test.com/status")
            request.set_success_url("https://test.com/success")
            request.set_error_url("https://test.com/error")
            request.set_awaiting_url("https://test.com/awaiting")
            request.set_cancel_url("https://test.com/cancel")

            # Step 3 - Send Payment Request
            result = H2HPaymentAdapter(credentials).send_h2h_pre_authorization_request(request)
            print(result.get_notification().get_redirect_url())
        except FieldException as field_exception:
            print(field_exception)

if __name__ == "__main__":
    PreAuthorization.send_pre_authorization_payment_request()
```

Note: It's important to note that the status of the transaction, whether it's a success or an error, will be communicated asynchronously via a webhook notification. Within the SDK, we've included a method to create a webhook and notification handler, enabling you to receive these transaction notifications efficiently and take action. This allows for real-time updates on transaction statuses directly within your application.

## Capture Pre-Authorization

Sending a normal Pre-Authorization H2H request.

### Step 1: Refer to Common Prerequisite

Before proceeding with the Pre-Authorization Request, please refer to the [Common Prerequisite: Creating Credentials section](#common-prerequisite-creating-credentials-object) at the beginning of this documentation for the initial setup of the SDK credentials. Ensure you have correctly configured your credentials as described there.

### Step 2: Creating Payment Parameter Object

In this step, we will provide the SDK with the payment parameters:

- Merchant Transaction Id
- Payment Solution
- Transaction Id

```python
from sdk.models.requests.h2h.h2h_pre_authorization_capture import H2HPreAuthorizationCapture
from sdk.enums.payment_solutions import PaymentSolutions

request = H2HPreAuthorizationCapture()
request.set_merchant_transaction_id("334198711")
request.set_payment_solution(PaymentSolutions.caixapucpuce)
request.set_transaction_id("31399103")
```

### Step 3: Send The H2H Capture Request and Retrieve Response

The response from the payment service can be handled using a custom response handler. Below is a code snippet showing how to send the Pre-Authorization capture request and retrieve the status.

```python
from sdk.adapters.h2h_payment_adapter import H2HPaymentAdapter
from sdk.exceptions.field_exception import FieldException

try:
    result = H2HPaymentAdapter(credentials).send_h2h_pre_authorization_capture(request)
    print(result.get_notification().operations[-1].status)
except FieldException as field_exception:
    print(field_exception)
```

### Complete Example

Here is the complete example combining all the sections, including the creation of credentials, configuration of payment parameters, and sending the capture request.

```python
from sdk.adapters.h2h_payment_adapter import H2HPaymentAdapter
from sdk.enums.environment import Environment
from sdk.enums.payment_solutions import PaymentSolutions
from sdk.exceptions.field_exception import FieldException
from sdk.models.credentials import Credentials
from sdk.models.requests.h2h.h2h_pre_authorization_capture import H2HPreAuthorizationCapture

class Capture:

    @staticmethod
    def send_capture_payment_request():
        try:
            # Step 1 - Creating Credentials Object
            credentials = Credentials()
            credentials.set_merchant_id("your_merchant_id")
            credentials.set_merchant_pass("your_merchant_pass")
            credentials.set_environment(Environment.STAGING)
            credentials.set_product_id("your_product_id")
            credentials.set_api_version(5)

            # Step 2 - Configure Payment Parameters
            request = H2HPreAuthorizationCapture()
            request.set_merchant_transaction_id("334198711")
            request.set_payment_solution(PaymentSolutions.caixapucpuce)
            request.set_transaction_id("31399103")

            # Step 3 - Send Payment Request
            result = H2HPaymentAdapter(credentials).send_h2h_pre_authorization_capture(request)
            print(result.get_notification().operations[-1].status)
        except FieldException as field_exception:
            print(field_exception)

if __name__ == "__main__":
    Capture.send_capture_payment_request()
```

Note: It's important to note that the status of the transaction, whether it's a success or an error, will be communicated asynchronously via a webhook notification. Within the SDK, we've included a method to create a webhook and notification handler, enabling you to receive these transaction notifications efficiently and take action. This allows for real-time updates on transaction statuses directly within your application.

## Void Pre-Authorization

Sending a normal Void Pre-Authorization H2H request.

### Step 1: Refer to Common Prerequisite

Before proceeding with the Void Request, please refer to the [Common Prerequisite: Creating Credentials section](#common-prerequisite-creating-credentials-object) at the beginning of this documentation for the initial setup of the SDK credentials. Ensure you have correctly configured your credentials as described there.

### Step 

2: Creating Payment Parameter Object

In this step, we will provide the SDK with the payment parameters:

- Merchant Transaction Id
- Payment Solution
- Transaction Id

```python
from sdk.models.requests.h2h.h2h_void import H2HVoid
from sdk.enums.payment_solutions import PaymentSolutions

request = H2HVoid()
request.set_merchant_transaction_id("34455122231")
request.set_payment_solution(PaymentSolutions.creditcards)
request.set_transaction_id("3445512221")
```

### Step 3: Send The H2H Void Request and Retrieve Response

The response from the payment service can be handled using a custom response handler. Below is a code snippet showing how to send the Void request and retrieve the status.

```python
from sdk.adapters.h2h_payment_adapter import H2HPaymentAdapter
from sdk.exceptions.field_exception import FieldException

try:
    result = H2HPaymentAdapter(credentials).send_h2h_void_request(request)
    print(result.get_notification().operations[-1].status)
except FieldException as field_exception:
    print(field_exception)
```

### Complete Example

Here is the complete example combining all the sections, including the creation of credentials, configuration of payment parameters, and sending the Void request.

```python
from sdk.adapters.h2h_payment_adapter import H2HPaymentAdapter
from sdk.enums.environment import Environment
from sdk.enums.payment_solutions import PaymentSolutions
from sdk.exceptions.field_exception import FieldException
from sdk.models.credentials import Credentials
from sdk.models.requests.h2h.h2h_void import H2HVoid

class Void:

    @staticmethod
    def send_void_payment_request():
        try:
            # Step 1 - Creating Credentials Object
            credentials = Credentials()
            credentials.set_merchant_id("your_merchant_id")
            credentials.set_merchant_pass("your_merchant_pass")
            credentials.set_environment(Environment.STAGING)
            credentials.set_product_id("your_product_id")
            credentials.set_api_version(5)

            # Step 2 - Configure Payment Parameters
            request = H2HVoid()
            request.set_merchant_transaction_id("34455122231")
            request.set_payment_solution(PaymentSolutions.creditcards)
            request.set_transaction_id("3445512221")

            # Step 3 - Send Payment Request
            result = H2HPaymentAdapter(credentials).send_h2h_void_request(request)
            print(result.get_notification().operations[-1].status)
        except FieldException as field_exception:
            print(field_exception)

if __name__ == "__main__":
    Void.send_void_payment_request()
```

Note: It's important to note that the status of the transaction, whether it's a success or an error, will be communicated asynchronously via a webhook notification. Within the SDK, we've included a method to create a webhook and notification handler, enabling you to receive these transaction notifications efficiently and take action. This allows for real-time updates on transaction statuses directly within your application.

## Recurrent Initial

Sending a Recurrent Initial H2H request.

### Step 1: Refer to Common Prerequisite

Before proceeding with the Recurrent Initial Request, please refer to the [Common Prerequisite: Creating Credentials section](#common-prerequisite-creating-credentials-object) at the beginning of this documentation for the initial setup of the SDK credentials. Ensure you have correctly configured your credentials as described there.

### Step 2: Creating Payment Parameter Object

In this step, we will provide the SDK with the payment parameters:

- Amount
- Currency
- Country
- Customer Id
- Merchant Transaction Id
- Payment Solution
- Payment Recurring Type
- ChName
- CardNumber
- ExpDate
- CvnNumber
- Status URL
- Error URL
- Success URL
- Cancel URL
- Awaiting URL

```python
from sdk.models.requests.h2h.h2h_payment_recurrent_initial import H2HPaymentRecurrentInitial
from sdk.enums.currency import Currency
from sdk.enums.country_code import CountryCodeAlpha2
from sdk.enums.payment_solutions import PaymentSolutions
from sdk.enums.payment_recurring_type import PaymentRecurringType

request = H2HPaymentRecurrentInitial()
request.set_amount("50")
request.set_currency(Currency.EUR)
request.set_country(CountryCodeAlpha2.ES)
request.set_customer_id("903")
request.set_merchant_transaction_id("64884555")
request.set_ch_name("Pablo")
request.set_card_number("4907270002222227")
request.set_cvn_number("123")
request.set_exp_date("0230")
request.set_payment_recurring_type(PaymentRecurringType.newCof)
request.set_payment_solution(PaymentSolutions.creditcards)
request.set_status_url("https://test.com/status")
request.set_success_url("https://test.com/success")
request.set_error_url("https://test.com/error")
request.set_awaiting_url("https://test.com/awaiting")
request.set_cancel_url("https://test.com/cancel")
request.set_force_token_request(True)
```

### Step 3: Send The H2H Recurrent Initial Request and Retrieve Response

The response from the payment service can be handled using a custom response handler. Below is a code snippet showing how to send the Recurrent Initial request and retrieve the redirection URL.

```python
from sdk.adapters.h2h_payment_adapter import H2HPaymentAdapter
from sdk.exceptions.field_exception import FieldException

try:
    result = H2HPaymentAdapter(credentials).send_h2h_payment_recurrent_initial(request)
    print(result.get_notification().get_redirect_url())
except FieldException as field_exception:
    print(field_exception)
```

### Complete Example

Here is the complete example combining all the sections, including the creation of credentials, configuration of payment parameters, and sending the Recurrent Initial request.

```python
from sdk.adapters.h2h_payment_adapter import H2HPaymentAdapter
from sdk.enums.country_code import CountryCodeAlpha2
from sdk.enums.currency import Currency
from sdk.enums.environment import Environment
from sdk.enums.payment_recurring_type import PaymentRecurringType
from sdk.enums.payment_solutions import PaymentSolutions
from sdk.exceptions.field_exception import FieldException
from sdk.models.credentials import Credentials
from sdk.models.requests.h2h.h2h_payment_recurrent_initial import H2HPaymentRecurrentInitial

class Recurring:

    @staticmethod
    def send_recurring_payment_request():
        try:
            # Step 1 - Creating Credentials Object
            credentials = Credentials()
            credentials.set_merchant_id("your_merchant_id")
            credentials.set_merchant_pass("your_merchant_pass")
            credentials.set_environment(Environment.STAGING)
            credentials.set_product_id("your_product_id")
            credentials.set_api_version(5)

            # Step 2 - Configure Payment Parameters
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
            request.set_status_url("https://test.com/status")
            request.set_success_url("https://test.com/success")
            request.set_error_url("https://test.com/fail")
            request.set_awaiting_url("https://test.com/await")
            request.set_cancel_url("https://test.com/cancel")
            request.set_payment_recurring_type(PaymentRecurringType.newCof)
            request.set_force_token_request(True)

            # Step 3 - Send Payment Request
            result = H2HPaymentAdapter(credentials).send_h2h_payment_recurrent_initial(request)
            print(result.get_notification().get_redirect_url())
        except FieldException as field_exception:
            print(field_exception)

if __name__ == "__main__":
    Recurring.send_recurring_payment_request()
```

Note: It's important to note that the status of the transaction, whether it's a success or an error, will be communicated asynchronously via a webhook notification. Within the SDK, we've included a method to create a webhook and notification handler, enabling you to receive these transaction notifications efficiently and take action. This allows for real-time updates on transaction statuses directly within your application.

## Recurrent Subsequent

Sending a Recurrent Subsequent H2H request.

### Step 1: Refer to Common Prerequisite

Before proceeding with the Recurrent Subsequent Request, please refer to the [Common Prerequisite: Creating Credentials section](#common-prerequisite-creating-credentials-object) at the beginning of this documentation for the initial setup of the SDK credentials. Ensure you have correctly configured your credentials as described there.

### Step 2: Creating Payment Parameter Object

In this step, we will provide the SDK with the payment parameters:

- Subscription Plan
- Payment Recurring Type
- Merchant Exemptions Sca
- Customer Id
- Merchant Transaction Id
- Payment Solution
- Payment Recurring Type
- ChName
- Card Number Token

```python
from sdk.models.requests.h2h.h2h_payment_recurrent_successive import H2HPaymentRecurrentSuccessive
from sdk.enums.payment_solutions import PaymentSolutions
from sdk.enums.payment_recurring_type import PaymentRecurringType
from sdk.enums.merchant_exemptions_sca import MerchantExemptionsSca

request = H2HPaymentRecurrentSuccessive()
request.set_subscription_plan("613317123312")
request.set_payment_recurring_type(PaymentRecurringType.cof)
request.set_merchant_exemptions_sca(MerchantExemptionsSca.MIT)
request.set_card_number_token("51331223312")
request.set_customer_id("903")
request.set_ch_name("First name Last name")
request.set_payment_solution(PaymentSolutions.credit

cards)
```

### Step 3: Send The H2H Recurrent Subsequent Request and Retrieve Response

The response from the payment service can be handled using a custom response handler. Below is a code snippet showing how to send the Recurrent Subsequent request and retrieve the status.

```python
from sdk.adapters.h2h_payment_adapter import H2HPaymentAdapter
from sdk.exceptions.field_exception import FieldException

try:
    result = H2HPaymentAdapter(credentials).send_h2h_payment_recurrent_successive(request)
    print(result.get_notification().operations[-1].status)
except FieldException as field_exception:
    print(field_exception)
```

### Complete Example

Here is the complete example combining all the sections, including the creation of credentials, configuration of payment parameters, and sending the Recurrent Subsequent request.

```python
from sdk.adapters.h2h_payment_adapter import H2HPaymentAdapter
from sdk.enums.country_code import CountryCodeAlpha2
from sdk.enums.currency import Currency
from sdk.enums.environment import Environment
from sdk.enums.merchant_exemptions_sca import MerchantExemptionsSca
from sdk.enums.payment_recurring_type import PaymentRecurringType
from sdk.enums.payment_solutions import PaymentSolutions
from sdk.exceptions.field_exception import FieldException
from sdk.models.credentials import Credentials
from sdk.models.requests.h2h.h2h_payment_recurrent_successive import H2HPaymentRecurrentSuccessive

class RecurringSubsequent:

    @staticmethod
    def send_recurring_subsequent_payment_request():
        try:
            # Step 1 - Creating Credentials Object
            credentials = Credentials()
            credentials.set_merchant_id("your_merchant_id")
            credentials.set_merchant_pass("your_merchant_pass")
            credentials.set_environment(Environment.STAGING)
            credentials.set_product_id("your_product_id")
            credentials.set_api_version(5)

            # Step 2 - Configure Payment Parameters
            request = H2HPaymentRecurrentSuccessive()
            request.set_subscription_plan("613317123312")
            request.set_payment_recurring_type(PaymentRecurringType.cof)
            request.set_merchant_exemptions_sca(MerchantExemptionsSca.MIT)
            request.set_card_number_token("51331223312")
            request.set_customer_id("903")
            request.set_ch_name("First name Last name")
            request.set_payment_solution(PaymentSolutions.creditcards)

            # Step 3 - Send Payment Request
            result = H2HPaymentAdapter(credentials).send_h2h_payment_recurrent_successive(request)
            print(result.get_notification().operations[-1].status)
        except FieldException as field_exception:
            print(field_exception)

if __name__ == "__main__":
    RecurringSubsequent.send_recurring_subsequent_payment_request()
```

Note: It's important to note that the status of the transaction, whether it's a success or an error, will be communicated asynchronously via a webhook notification. Within the SDK, we've included a method to create a webhook and notification handler, enabling you to receive these transaction notifications efficiently and take action. This allows for real-time updates on transaction statuses directly within your application.

## Refund

Sending a normal Refund H2H request.

### Step 1: Refer to Common Prerequisite

Before proceeding with the Refund Request, please refer to the [Common Prerequisite: Creating Credentials section](#common-prerequisite-creating-credentials-object) at the beginning of this documentation for the initial setup of the SDK credentials. Ensure you have correctly configured your credentials as described there.

### Step 2: Creating Payment Parameter Object

In this step, we will provide the SDK with the payment parameters:

- Amount
- Merchant Transaction Id
- Payment Solution
- Transaction Id

```python
from sdk.models.requests.h2h.h2h_refund import H2HRefund
from sdk.enums.payment_solutions import PaymentSolutions

request = H2HRefund()
request.set_amount("10")
request.set_merchant_transaction_id("4144412231")
request.set_payment_solution(PaymentSolutions.creditcards)
request.set_transaction_id("45465466")
```

### Step 3: Send The H2H Refund Request and Retrieve Response

The response from the payment service can be handled using a custom response handler. Below is a code snippet showing how to send the Refund request and retrieve the status.

```python
from sdk.adapters.h2h_payment_adapter import H2HPaymentAdapter
from sdk.exceptions.field_exception import FieldException

try:
    result = H2HPaymentAdapter(credentials).send_h2h_refund_request(request)
    print(result.get_notification().operations[-1].status)
except FieldException as field_exception:
    print(field_exception)
```

### Complete Example

Here is the complete example combining all the sections, including the creation of credentials, configuration of payment parameters, and sending the Refund request.

```python
from sdk.adapters.h2h_payment_adapter import H2HPaymentAdapter
from sdk.enums.environment import Environment
from sdk.enums.payment_solutions import PaymentSolutions
from sdk.exceptions.field_exception import FieldException
from sdk.models.credentials import Credentials
from sdk.models.requests.h2h.h2h_refund import H2HRefund

class Refund:

    @staticmethod
    def send_refund_payment_request():
        try:
            # Step 1 - Creating Credentials Object
            credentials = Credentials()
            credentials.set_merchant_id("your_merchant_id")
            credentials.set_merchant_pass("your_merchant_pass")
            credentials.set_environment(Environment.STAGING)
            credentials.set_product_id("your_product_id")
            credentials.set_api_version(5)

            # Step 2 - Configure Payment Parameters
            request = H2HRefund()
            request.set_amount("10")
            request.set_merchant_transaction_id("4144412231")
            request.set_payment_solution(PaymentSolutions.creditcards)
            request.set_transaction_id("45465466")

            # Step 3 - Send Payment Request
            result = H2HPaymentAdapter(credentials).send_h2h_refund_request(request)
            print(result.get_notification().operations[-1].status)
        except FieldException as field_exception:
            print(field_exception)

if __name__ == "__main__":
    Refund.send_refund_payment_request()
```

Note: It's important to note that the status of the transaction, whether it's a success or an error, will be communicated asynchronously via a webhook notification. Within the SDK, we've included a method to create a webhook and notification handler, enabling you to receive these transaction notifications efficiently and take action. This allows for real-time updates on transaction statuses directly within your application.