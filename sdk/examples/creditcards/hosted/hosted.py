from sdk.adapters.hosted_payment_adapter import HostedPaymentAdapter
from sdk.enums.country_code import CountryCodeAlpha2
from sdk.enums.currency import Currency
from sdk.enums.environment import Environment
from sdk.enums.payment_solutions import PaymentSolutions
from sdk.exceptions.field_exception import FieldException
from sdk.models.credentials import Credentials
from sdk.models.requests.hosted.hosted_payment_redirection import HostedPaymentRedirection
from sdk.utils import creds


class Hosted:

    @staticmethod
    def send_hosted_payment_request():
        try:
            # Step 1 - Creating Credentials Object
            credentials = Credentials()
            credentials.set_environment(
                Environment.STAGING if creds.environment.lower() == "staging".lower() else Environment.PRODUCTION
            )
            credentials.set_merchant_id(creds.merchant_id)
            credentials.set_merchant_pass(creds.merchant_pass)
            credentials.set_product_id(creds.product_id)
            credentials.set_api_version(int(creds.api_version))

            # Step 2 - Configure Payment Parameters
            request = HostedPaymentRedirection()
            request.set_amount("50.4321")
            request.set_currency(Currency.EUR)
            request.set_country(CountryCodeAlpha2.ES)
            request.set_customer_id("903")
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
            result = HostedPaymentAdapter(credentials).send_hosted_payment_request(request)
            print(result.get_redirect_url())
        except FieldException as field_exception:
            print(field_exception)


if __name__ == "__main__":
    Hosted.send_hosted_payment_request()
