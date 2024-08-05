# Quick Start Guide for the Python SDK

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Creating Credentials Object](#creating-credentials-object)
- [Hosted Request](#hosted-request)
- [Webhook for Notifications](#webhook-for-notifications)
- [Complete Example](#complete-example)

## Introduction

This documentation provides a quick start guide to using our Python SDK for handling Hosted transactions. Hosted transactions involve sending payment details and displaying a web page from AddonPayments for the user to enter their card data and proceed with the transaction.

## Installation

The SDK will be provided as WHL file that can be installed using pip:

```sh
pip install payment_sdk-0.1-py3-none-any.whl
```

## Creating Credentials Object

First, instantiate the `Credentials` object with your merchant details. This includes your Merchant ID and Merchant Pass, which are essential for authenticating requests to the AddonPayments API.

### Steps

1. **Initialize Credentials Object:** Create a new instance of the `Credentials` class to hold the authentication and configuration details.
2. **Set Merchant ID:** Assign the merchant ID using the `set_merchant_id` method. This ID is provided by the payment service provider and identifies the merchant account.
3. **Set Merchant Password:** Assign the merchant password using the `set_merchant_pass` method. This password is provided by the payment service provider and is used for authentication.
4. **Set Environment:** Specify the environment (e.g., STAGING, PRODUCTION) using the `set_environment` method. This determines the endpoint URL for the payment requests.
5. **Set Product ID:** Assign the product ID using the `set_product_id` method. This ID identifies the specific product or service being paid for.
6. **Set API Version:** Specify the API version using the `set_api_version` method. This ensures compatibility with the payment service's API.
7. **Assign Credentials to Payment Service:** Finally, assign the configured credentials object to the credentials property of the payment service. This step is crucial as it links the payment service instance with the necessary authentication and configuration details, allowing it to authenticate and process payment requests.

```python
from sdk.models.Credentials import Credentials
from sdk.enums.Environment import Environment

credentials = Credentials()
credentials.set_merchant_id("your_merchant_id")
credentials.set_merchant_pass("your_merchant_pass")
credentials.set_environment(Environment.STAGING)
credentials.set_product_id("your_product_id")
credentials.set_api_version(5)
```

## Hosted Request

To send a normal payment request used in a normal payment scenario, follow the steps below.

### Step 1: Creating Payment Parameter Object

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
from sdk.models.requests.hosted.HostedPaymentRedirection import HostedPaymentRedirection
from sdk.enums.Currency import Currency
from sdk.enums.CountryCodeAlpha2 import CountryCodeAlpha2
from sdk.enums.PaymentSolutions import PaymentSolutions

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

### Step 2: Send The Hosted Request and Retrieve Response

The response from the payment service can be handled using a custom response handler. Below is a code snippet showing how to send the hosted payment request and retrieve the redirection URL.

```python
from sdk.adapters.HostedPaymentAdapter import HostedPaymentAdapter
from sdk.exceptions.FieldException import FieldException

try:
    result = HostedPaymentAdapter(credentials).send_hosted_payment_request(request)
    print(result.get_redirect_url())
except FieldException as field_exception:
    print(field_exception)
```

## Webhook for Notifications

It's important to note that the status of the transaction, whether it's a success or an error, will be communicated asynchronously via a webhook notification. Below is an example of how to set up a Flask application to handle webhook notifications and parse the notification data.

```python
from flask import Flask, request, jsonify
from sdk.notifications.NotificationAdapter import NotificationAdapter

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    xml_content = request.data.decode('utf-8')
    try:
        notification = NotificationAdapter.parse_notification(xml_content)

        # Example of parsing notification data
        operations = notification.operations
        for operation in operations:
            print(f"Service: {operation.service}, Status: {operation.status}")
        
        print(f"Transaction Status: {notification.status}")
        
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

if __name__ == "__main__":
    app.run(port=5000)
```

## Complete Example

Here is the complete example combining all the sections, including the creation of credentials, configuration of payment parameters, sending the payment request, and setting up a Flask application for webhook notifications. This example also demonstrates how to get data such as amount, customer ID, and merchant transaction ID from the user.

```python
from flask import Flask, request, jsonify
from sdk.adapters.HostedPaymentAdapter import HostedPaymentAdapter
from sdk.enums.CountryCodeAlpha2 import CountryCodeAlpha2
from sdk.enums.Currency import Currency
from sdk.enums.Environment import Environment
from sdk.enums.PaymentSolutions import PaymentSolutions
from sdk.exceptions.FieldException import FieldException
from sdk.models.Credentials import Credentials
from sdk.models.requests.hosted.HostedPaymentRedirection import HostedPaymentRedirection
from sdk.notifications.NotificationAdapter import NotificationAdapter

app = Flask(__name__)

@app.route('/pay', methods=['POST'])
def pay():
    try:
        data = request.json
        amount = data['amount']
        customer_id = data['customer_id']
        merchant_transaction_id = data['merchant_transaction_id']
        
        # Step 1 - Creating Credentials Object
        credentials = Credentials()
        credentials.set_merchant_id("your_merchant_id")
        credentials.set_merchant_pass("your_merchant_pass")
        credentials.set_environment(Environment.STAGING)
        credentials.set_product_id("your_product_id")
        credentials.set_api_version(5)

        # Step 2 - Configure Payment Parameters
        payment_request = HostedPaymentRedirection()
        payment_request.set_amount(amount)
        payment_request.set_currency(Currency.EUR)
        payment_request.set_country(CountryCodeAlpha2.ES)
        payment_request.set_customer_id(customer_id)
        payment_request.set_merchant_transaction_id(merchant_transaction_id)
        payment_request.set_payment_solution(PaymentSolutions.creditcards)
        payment_request.set_status_url("https://test.com/status")
        payment_request.set_success_url("https://test.com/success")
        payment_request.set_error_url("https://test.com/error")
        payment_request.set_awaiting_url("https://test.com/awaiting")
        payment_request.set_cancel_url("https://test.com/cancel")
        payment_request.set_force_token_request(False)

        # Step 3 - Send Payment Request
        result = HostedPaymentAdapter(credentials).send_hosted_payment_request(payment_request)
        return jsonify({'redirect_url': result.get_redirect_url()}), 200
    except FieldException as field_exception:
        return jsonify({'error': str(field_exception)}), 400
    except KeyError as e:
        return jsonify({'error': f'Missing parameter: {str(e)}'}), 400

@app.route('/webhook', methods=['POST'])
def webhook():
    xml_content = request.data.decode('utf-8')
    try:
        notification = NotificationAdapter.parse_notification(xml_content)

        # Example of parsing notification data
        operations = notification.operations
        for operation in operations:
            print(f"Service: {operation.service}, Status: {operation.status}")
        
        print(f"Transaction Status: {notification.status}")
        
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

if __name__ == "__main__":
    app.run(port=5000)
```