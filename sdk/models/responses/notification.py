from dataclasses import dataclass, field
from typing import Optional, List
from dataclasses_json import dataclass_json, config, Undefined
from sdk.enums.currency import Currency
from sdk.enums.operation_types import OperationTypes
from sdk.enums.payment_solutions import PaymentSolutions
from sdk.enums.transaction import TransactionResult


class ParsingUtils:

    @staticmethod
    def parse_json_to_entries(data: dict):
        """Custom parser to convert flat JSON dict into a list of Entry objects"""
        entries = []
        if data:
            for k, v in data.items():
                entries.append(Entry(key=k, value=v))
        return entries

    @staticmethod
    def parse_extra_details(data: dict) -> 'ExtraDetails':
        entries = ParsingUtils.parse_json_to_entries(data)
        return ExtraDetails(entry=entries)


    @staticmethod
    def parse_optional_trx_params(data: dict) -> 'OptionalTransactionParams':
        entries = ParsingUtils.parse_json_to_entries(data)
        return OptionalTransactionParams(entry=entries)


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
class Entry:
    key: Optional[str] = None
    value: Optional[str] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class ExtraDetails:
    entry: Optional[List[Entry]] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class OptionalTransactionParams:
    entry: Optional[List[Entry]] = None


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
    extraDetails: Optional[ExtraDetails] = field(
        default=None, metadata=config(decoder=ParsingUtils.parse_extra_details)
    )


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
    optionalTransactionParams: Optional[OptionalTransactionParams] = field(
        default=None, metadata=config(decoder=ParsingUtils.parse_optional_trx_params)
    )


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Notification:
    message: Optional[str] = None
    status: Optional[str] = None
    operations: Optional[List[Operation]] = field(default=None, metadata=config(field_name="operationsArray"))
    workFlowResponse: Optional[WorkFlowResponse] = None
    optionalTransactionParams: Optional[OptionalTransactionParams] = field(
        default=None, metadata=config(decoder=ParsingUtils.parse_optional_trx_params)
    )

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

    def get_entry(self, entry_key: str):
        if (self.operations is None or self.operations[0].paymentDetails is None
                or self.operations[0].paymentDetails.extraDetails is None
                or self.operations[0].paymentDetails.extraDetails.entry is None):
            return None
        else:
            entries = self.operations[0].paymentDetails.extraDetails.entry
            search_string = entry_key.lower()
            result = next((entry for entry in entries if entry.key.lower() == search_string), None)
            return result.value if result is not None else None

    def get_nemuru_txn_id(self) -> Optional[str]:
        return self.get_entry("nemuruTxnId")

    def get_nemuru_cart_hash(self) -> Optional[str]:
        return self.get_entry("nemuruCartHash")

    def get_nemuru_auth_token(self) -> Optional[str]:
        return self.get_entry("nemuruAuthToken")

    def get_nemuru_disable_form_edition(self) -> Optional[str]:
        return self.get_entry("nemuruDisableFormEdition")

    def get_status(self) -> Optional[str]:
        return self.get_entry("status")

    def get_disable_form_edition(self) -> Optional[str]:
        return self.get_entry("disableFormEdition")

    def get_merchant_transaction_id(self) -> Optional[str]:
        if self.operations is None:
            return None
        return self.operations[-1].merchantTransactionId

    def get_transaction_result(self) -> Optional[TransactionResult]:
        if self.operations is None:
            return None
        try:
            return TransactionResult.get_by_status(self.operations[-1].status.upper())
        except KeyError:
            return None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Response:
    response: Optional[Notification] = None
