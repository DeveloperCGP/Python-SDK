from sdk.adapters.js_payment_adapter import JSPaymentAdapter
from sdk.enums.country_code import CountryCodeAlpha2
from sdk.enums.currency import Currency
from sdk.enums.environment import Environment
from sdk.enums.operation_types import OperationTypes
from sdk.enums.payment_solutions import PaymentSolutions
from sdk.exceptions.field_exception import FieldException
from sdk.models.credentials import Credentials
from sdk.models.requests.js.js_charge import JSCharge
from sdk.utils import creds


class Charge:

    @staticmethod
    def send_charge_payment_request():
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
            request = JSCharge()
            request.set_amount("30")
            request.set_prepay_token("45357b66-8f04-4276-84f4-d35c885bde8e")
            request.set_country(CountryCodeAlpha2.ES)
            request.set_customer_id("55")
            request.set_currency(Currency.EUR)
            request.set_operation_type(OperationTypes.DEBIT)
            request.set_payment_solution(PaymentSolutions.creditcards)
            request.set_status_url(creds.status_url)
            request.set_success_url(creds.success_url)
            request.set_error_url(creds.error_url)
            request.set_awaiting_url(creds.awaiting_url)
            request.set_cancel_url(creds.cancel_url)

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
