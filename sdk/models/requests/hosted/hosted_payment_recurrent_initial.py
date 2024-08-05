from sdk.enums.challenge_ind import ChallengeInd
from sdk.enums.payment_recurring_type import PaymentRecurringType
from sdk.models.requests.hosted.hosted_payment_redirection import HostedPaymentRedirection


class HostedPaymentRecurrentInitial(HostedPaymentRedirection):
    __paymentRecurringType: PaymentRecurringType = PaymentRecurringType.newCof
    __challengeInd: str = None

    def __init__(self):
        super().__init__()
        self.__paymentRecurringType = PaymentRecurringType.newCof

    def get_payment_recurring_type(self) -> PaymentRecurringType:
        return self.__paymentRecurringType

    def set_payment_recurring_type(self, payment_recurring_type: PaymentRecurringType):
        self.__paymentRecurringType = payment_recurring_type

    def get_challenge_ind(self) -> ChallengeInd:
        return ChallengeInd.get_challenge_ind(self.__challengeInd)

    def set_challenge_ind(self, challenge_ind: ChallengeInd):
        self.__challengeInd = challenge_ind.value
