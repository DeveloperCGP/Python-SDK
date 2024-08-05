from sdk.enums.challenge_ind import ChallengeInd
from sdk.enums.payment_recurring_type import PaymentRecurringType
from sdk.models.requests.js.js_charge import JSCharge


class JSPaymentRecurrentInitial(JSCharge):
    """
    JSPaymentRecurrentInitial
    """
    __paymentRecurringType: PaymentRecurringType = None
    __challengeInd: str = None

    def __init__(self):
        super().__init__()
        self.__paymentRecurringType = PaymentRecurringType.newCof
        self.__challengeInd = ChallengeInd.CI_04.value

    def get_payment_recurring_type(self) -> PaymentRecurringType:
        return self.__paymentRecurringType

    def set_payment_recurring_type(self, payment_recurring_type: PaymentRecurringType) -> None:
        self.__paymentRecurringType = payment_recurring_type

    def get_challenge_ind(self) -> ChallengeInd:
        return ChallengeInd[self.__challengeInd]

    def set_challenge_ind(self, challenge_ind: ChallengeInd) -> None:
        self.__challengeInd = challenge_ind.value

    def to_dict(self):
        dict_with_none = {
            "paymentRecurringType": self.__paymentRecurringType.value
            if self.__paymentRecurringType is not None else None,
            "challengeInd": self.__challengeInd
        }
        dict_with_none.update(super().to_dict())

        return {k: v for k, v in dict_with_none.items() if v is not None}
