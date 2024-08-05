from sdk.enums.challenge_ind import ChallengeInd
from sdk.enums.payment_recurring_type import PaymentRecurringType
from sdk.models.requests.h2h.h2h_redirection import H2HRedirection


class H2HPaymentRecurrentInitial(H2HRedirection):
    __paymentRecurringType: PaymentRecurringType = PaymentRecurringType.newCof
    __challengeInd: str = None

    def __init__(self):
        super().__init__()
        self.__paymentRecurringType = PaymentRecurringType.newCof

    def get_payment_recurring_type(self):
        return self.__paymentRecurringType

    def set_payment_recurring_type(self, new_payment_recurring_type: PaymentRecurringType):
        self.__paymentRecurringType = new_payment_recurring_type

    def get_challenge_ind(self):
        return ChallengeInd.get_challenge_ind(self.__challengeInd)

    def set_challenge_ind(self, new_challenge_ind: ChallengeInd):
        self.__challengeInd = new_challenge_ind.value
