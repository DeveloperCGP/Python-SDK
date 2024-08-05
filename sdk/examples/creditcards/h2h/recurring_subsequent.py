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
from sdk.utils import creds


class RecurringSubsequent:

    @staticmethod
    def send_recurring_subsequent_payment_request():
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
            request = H2HPaymentRecurrentSuccessive()
            request.set_amount("50")
            request.set_currency(Currency.EUR)
            request.set_country(CountryCodeAlpha2.ES)
            request.set_customer_id("55")
            request.set_ch_name("First name Last name")
            request.set_payment_solution(PaymentSolutions.creditcards)
            request.set_card_number_token("6529405841342227")
            request.set_subscription_plan("301676347745850")
            request.set_status_url(creds.status_url)
            request.set_success_url(creds.success_url)
            request.set_error_url(creds.error_url)
            request.set_awaiting_url(creds.awaiting_url)
            request.set_cancel_url(creds.cancel_url)
            request.set_payment_recurring_type(PaymentRecurringType.cof)
            request.set_merchant_exemptions_sca(MerchantExemptionsSca.MIT)

            # Step 3 - Send Payment Request
            result = H2HPaymentAdapter(credentials).send_h2h_payment_recurrent_successive(request)
            print(result.get_notification().operations[-1].status)

        except FieldException as field_exception:
            print(field_exception)


if __name__ == "__main__":
    RecurringSubsequent.send_recurring_subsequent_payment_request()
