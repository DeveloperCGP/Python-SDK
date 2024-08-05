from sdk.adapters.h2h_payment_adapter import H2HPaymentAdapter
from sdk.enums.environment import Environment
from sdk.enums.payment_solutions import PaymentSolutions
from sdk.exceptions.field_exception import FieldException
from sdk.models.credentials import Credentials
from sdk.models.requests.h2h.h2h_refund import H2HRefund
from sdk.utils import creds


class Refund:

    @staticmethod
    def send_refund_payment_request():
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
            request = H2HRefund()
            request.set_amount("20")
            request.set_payment_solution(PaymentSolutions.caixapucpuce)
            request.set_merchant_transaction_id("38559715")
            request.set_transaction_id("7817556")

            # Step 3 - Send Payment Request
            result = H2HPaymentAdapter(credentials).send_h2h_refund_request(request)
            print(result.get_notification().operations[-1].status)

        except FieldException as field_exception:
            print(field_exception)


if __name__ == "__main__":
    Refund.send_refund_payment_request()
