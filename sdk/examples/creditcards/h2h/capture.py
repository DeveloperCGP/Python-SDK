from sdk.adapters.h2h_payment_adapter import H2HPaymentAdapter
from sdk.enums.environment import Environment
from sdk.enums.payment_solutions import PaymentSolutions
from sdk.exceptions.field_exception import FieldException
from sdk.models.credentials import Credentials
from sdk.models.requests.h2h.h2h_pre_authorization_capture import H2HPreAuthorizationCapture
from sdk.utils import creds


class Capture:

    @staticmethod
    def send_capture_payment_request():
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
            request = H2HPreAuthorizationCapture()
            request.set_payment_solution(PaymentSolutions.caixapucpuce)
            request.set_transaction_id("7961829")
            request.set_merchant_transaction_id("344122331")

            # Step 3 - Send Payment Request
            result = H2HPaymentAdapter(credentials).send_h2h_pre_authorization_capture(request)
            print(result.get_notification().operations[-1].status)
            
        except FieldException as field_exception:
            print(field_exception)


if __name__ == "__main__":
    Capture().send_capture_payment_request()
