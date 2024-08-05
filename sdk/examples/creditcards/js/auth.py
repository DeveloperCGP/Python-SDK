from sdk.adapters.js_payment_adapter import JSPaymentAdapter
from sdk.enums.country_code import CountryCodeAlpha2
from sdk.enums.currency import Currency
from sdk.enums.environment import Environment
from sdk.enums.operation_types import OperationTypes
from sdk.exceptions.field_exception import FieldException
from sdk.models.credentials import Credentials
from sdk.models.requests.js.js_authorization_request import JSAuthorizationRequest
from sdk.utils import creds


class Auth:

    @staticmethod
    def send_auth_payment_request():
        try:
            # Step 1 - Creating Credentials Object
            credentials = Credentials()
            credentials.set_environment(
                Environment.STAGING if creds.environment.lower() == "staging".lower() else Environment.PRODUCTION
            )
            credentials.set_merchant_id(creds.merchant_id)
            credentials.set_merchant_key(creds.merchant_key)
            credentials.set_merchant_pass(creds.merchant_pass)
            credentials.set_product_id(creds.product_id)
            credentials.set_api_version(int(creds.api_version))

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
