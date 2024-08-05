from dataclasses import dataclass, field
from typing import Optional, List

from dataclasses_json import dataclass_json, config, Undefined

from sdk.enums.currency import Currency
from sdk.enums.operation_types import OperationTypes
from sdk.enums.payment_solutions import PaymentSolutions
from sdk.enums.transaction import TransactionResult


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class ResponseCode:
    code: Optional[str] = None
    message: Optional[str] = None
    uuid: Optional[str] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Mpi:
    acsTransID: Optional[str] = None
    authMethod: Optional[str] = None
    authTimestamp: Optional[str] = None
    authenticationStatus: Optional[str] = None
    cavv: Optional[str] = None
    eci: Optional[str] = None
    messageVersion: Optional[str] = None
    threeDSSessionData: Optional[str] = None
    threeDSv2Token: Optional[str] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class ExtraDetails:
    nemuruTxnId: Optional[str] = None
    nemuruCartHash: Optional[str] = None
    nemuruAuthToken: Optional[str] = None
    nemuruDisableFormEdition: Optional[str] = None
    status: Optional[str] = None
    disableFormEdition: Optional[str] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class PaymentDetails:
    cardNumberToken: Optional[str] = None
    account: Optional[str] = None
    cardHolderName: Optional[str] = None
    cardNumber: Optional[str] = None
    cardType: Optional[str] = None
    expDate: Optional[str] = None
    issuerBank: Optional[str] = None
    issuerCountry: Optional[str] = None
    extraDetails: Optional[ExtraDetails] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Entry:
    key: Optional[str] = None
    value: Optional[str] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class WorkFlowResponse:
    id: Optional[str] = None
    name: Optional[str] = None
    version: Optional[str] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Operation:
    amount: Optional[float] = None
    currency: Optional[Currency] = None
    details: Optional[str] = None
    merchantTransactionId: Optional[str] = None
    paySolTransactionId: Optional[str] = None
    service: Optional[str] = None
    status: Optional[str] = None
    transactionId: Optional[str] = None
    respCode: Optional[ResponseCode] = None
    operationType: Optional[OperationTypes] = None
    paymentDetails: Optional[PaymentDetails] = None
    mpi: Optional[Mpi] = None
    paymentCode: Optional[str] = None
    paymentMessage: Optional[str] = None
    message: Optional[str] = None
    paymentMethod: Optional[str] = None
    paymentSolution: Optional[PaymentSolutions] = None
    authCode: Optional[str] = None
    rad: Optional[str] = None
    radMessage: Optional[str] = None
    redirectionResponse: Optional[str] = None
    subscriptionPlan: Optional[str] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Notification:
    message: Optional[str] = None
    status: Optional[str] = None
    operations: Optional[List[Operation]] = field(default=None, metadata=config(field_name="operationsArray"))
    workFlowResponse: Optional[WorkFlowResponse] = None

    def is_last_notification(self) -> bool:
        if self.operations is None:
            return False
        return self.operations[-1].status.lower() == "SUCCESS".lower() or self.operations[
            -1].status.lower() == "ERROR".lower()

    def get_redirect_url(self) -> Optional[str]:
        if self.operations is None:
            return None
        redirection_url = self.operations[-1].redirectionResponse
        if redirection_url is not None and len(redirection_url) > 0:
            return redirection_url.replace("redirect:", "")
        return None

    def get_nemuru_cart_hash(self) -> Optional[str]:
        if self.operations is None:
            return None
        if self.operations is not None and self.operations[0].paymentDetails is not None \
                and self.operations[0].paymentDetails.extraDetails is not None:
            return self.operations[0].paymentDetails.extraDetails.nemuruCartHash
        else:
            return None

    def get_nemuru_auth_token(self) -> Optional[str]:
        if self.operations is None:
            return None
        if self.operations is not None and self.operations[0].paymentDetails is not None \
                and self.operations[0].paymentDetails.extraDetails is not None:
            return self.operations[0].paymentDetails.extraDetails.nemuruAuthToken
        else:
            return None

    def get_merchant_transaction_id(self) -> Optional[str]:
        if self.operations is None:
            return None
        return self.operations[-1].merchantTransactionId

    def get_transaction_result(self) -> Optional[TransactionResult]:
        if self.operations is None:
            return None
        try:
            return TransactionResult[self.operations[-1].status.upper()]
        except KeyError:
            return None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Response:
    response: Optional[Notification] = None
