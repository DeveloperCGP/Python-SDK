from typing import Tuple

from sdk.enums.merchant_exemptions_sca import MerchantExemptionsSca
from sdk.enums.payment_recurring_type import PaymentRecurringType
from sdk.models.credentials import Credentials
from sdk.models.requests.h2h.h2h_redirection import H2HRedirection
from sdk.utils.general_utils import GeneralUtils


class H2HPaymentRecurrentSuccessive(H2HRedirection):
    __subscriptionPlan: str = None
    __paymentRecurringType: PaymentRecurringType = PaymentRecurringType.cof
    __merchantExemptionsSca: MerchantExemptionsSca = None

    def __init__(self):
        super().__init__()
        self.__paymentRecurringType = PaymentRecurringType.cof

    def get_subscription_plan(self):
        return self.__subscriptionPlan

    def set_subscription_plan(self, new_subscription_plan: str):
        self.__subscriptionPlan = new_subscription_plan

    def get_payment_recurring_type(self):
        return self.__paymentRecurringType

    def set_payment_recurring_type(self, new_payment_recurring_type: PaymentRecurringType):
        self.__paymentRecurringType = new_payment_recurring_type

    def get_merchant_exemptions_sca(self):
        return self.__merchantExemptionsSca

    def set_merchant_exemptions_sca(self, new_merchant_exemptions_sca: MerchantExemptionsSca):
        self.__merchantExemptionsSca = new_merchant_exemptions_sca

    def is_missing_field(self) -> Tuple[bool, any]:
        mandatory_fields = {
            "cardNumberToken": self.get_card_number_token(),
            "subscriptionPlan": self.get_subscription_plan(),
            "paymentRecurringType": self.get_payment_recurring_type(),
            "merchantExemptionsSca": self.__merchantExemptionsSca
        }

        is_missing_field = GeneralUtils.contains_null(mandatory_fields)

        if is_missing_field[0]:
            return is_missing_field
        else:
            return super().is_missing_field()

    def check_credentials(self, credentials: Credentials) -> Tuple[bool, any]:
        if credentials.get_api_version() < 0:
            return True, "apiVersion"

        mandatory_fields = {
            "merchantId": credentials.get_merchant_id(),
            "productId": credentials.get_product_id(),
            "merchantPass": credentials.get_merchant_pass(),
            "environment": credentials.get_environment().value
        }

        return GeneralUtils.contains_null(mandatory_fields)
