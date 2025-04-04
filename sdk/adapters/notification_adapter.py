import json
import xml.etree.ElementTree as ElementTree
from sdk.models.responses.notification import *


def parse_notification(notification_string: str) -> Optional[Notification]:
    try:
        if notification_string[0] == '<':
            root = ElementTree.fromstring(notification_string)
            return __xml_to_dataclass(root)
        else:
            data = json.loads(notification_string)
            print(data)
            if str(data["response"])[0] == '<':
                root = ElementTree.fromstring(data["response"])
                return __xml_to_dataclass(root)
            return Response.from_json(notification_string).response
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def __get_text(element, tag):
    found = element.find(tag)
    return found.text if found is not None else None


def __get_enum_value(cls, str_value: str):
    try:
        return cls[str_value] if str_value is not None else None
    except KeyError:
        return None


def __xml_to_dataclass(element):
    if element is None:
        return None
    if element.tag == "response" or element.tag == "payfrex-response":
        return Notification(
            message=__get_text(element, "message"),
            status=__get_text(element, "status"),
            operations=[__xml_to_dataclass(op) for op in element.find("operations")],
            workFlowResponse=__xml_to_dataclass(element.find("workFlowResponse")),
            optionalTransactionParams=__xml_to_dataclass(element.find("optionalTransactionParams")),
        )
    elif element.tag == "operation":
        return Operation(
            amount=float(__get_text(element, "amount")) if __get_text(element, "amount") else None,
            currency=__get_enum_value(Currency, __get_text(element, "currency")),
            details=__get_text(element, "details"),
            merchantTransactionId=__get_text(element, "merchantTransactionId"),
            paySolTransactionId=__get_text(element, "paySolTransactionId"),
            service=__get_text(element, "service"),
            status=__get_text(element, "status"),
            transactionId=__get_text(element, "transactionId"),
            respCode=__xml_to_dataclass(element.find("respCode")),
            operationType=__get_enum_value(OperationTypes, __get_text(element, "operationType")),
            paymentDetails=__xml_to_dataclass(element.find("paymentDetails")),
            mpi=__xml_to_dataclass(element.find("mpi")),
            paymentCode=__get_text(element, "paymentCode"),
            paymentMessage=__get_text(element, "paymentMessage"),
            message=__get_text(element, "message"),
            paymentMethod=__get_text(element, "paymentMethod"),
            paymentSolution=__get_enum_value(PaymentSolutions, __get_text(element, "paymentSolution")),
            authCode=__get_text(element, "authCode"),
            rad=__get_text(element, "rad"),
            radMessage=__get_text(element, "radMessage"),
            redirectionResponse=__get_text(element, "redirectionResponse"),
            subscriptionPlan=__get_text(element, "subscriptionPlan"),
            optionalTransactionParams=__xml_to_dataclass(element.find("optionalTransactionParams")),
        )
    elif element.tag == "respCode":
        return ResponseCode(
            code=__get_text(element, "code"),
            message=__get_text(element, "message"),
            uuid=__get_text(element, "uuid"),
        )
    elif element.tag == "paymentDetails":
        return PaymentDetails(
            cardNumberToken=__get_text(element, "cardNumberToken"),
            account=__get_text(element, "account"),
            cardHolderName=__get_text(element, "cardHolderName"),
            cardNumber=__get_text(element, "cardNumber"),
            cardType=__get_text(element, "cardType"),
            expDate=__get_text(element, "expDate"),
            issuerBank=__get_text(element, "issuerBank"),
            issuerCountry=__get_text(element, "issuerCountry"),
            extraDetails=__xml_to_dataclass(element.find("extraDetails")),
        )
    elif element.tag == "extraDetails":
        xml_dict = xml_to_dict(element)
        return ExtraDetails(
            entry=[__xml_to_dataclass(entry) for entry in element],
        ) if xml_dict is not None else ExtraDetails()
    elif element.tag == "optionalTransactionParams":
        xml_dict = xml_to_dict(element)
        return OptionalTransactionParams(
            entry=[__xml_to_dataclass(entry) for entry in element],
        ) if xml_dict is not None else OptionalTransactionParams()
    elif element.tag == "entry":
        xml_dict = xml_to_dict(element)
        return Entry(
            key=xml_dict["key"], value=xml_dict["value"]
        )
    elif element.tag == "mpi":
        return Mpi(
            acsTransID=__get_text(element, "acsTransID"),
            authMethod=__get_text(element, "authMethod"),
            authTimestamp=__get_text(element, "authTimestamp"),
            authenticationStatus=__get_text(element, "authenticationStatus"),
            cavv=__get_text(element, "cavv"),
            eci=__get_text(element, "eci"),
            messageVersion=__get_text(element, "messageVersion"),
            threeDSSessionData=__get_text(element, "threeDSSessionData"),
            threeDSv2Token=__get_text(element, "threeDSv2Token"),
        )
    elif element.tag == "workFlowResponse":
        return WorkFlowResponse(
            id=__get_text(element, "id"),
            name=__get_text(element, "name"),
            version=__get_text(element, "version"),
        )


def xml_to_dict(element):
    if len(element) == 0:  # If the element has no children
        return element.text
    result = {}
    for child in element:
        if child.tag not in result:
            result[child.tag] = xml_to_dict(child)
        else:
            if not isinstance(result[child.tag], list):
                result[child.tag] = [result[child.tag]]
            result[child.tag].append(xml_to_dict(child))
    return result


def get_extra_details_items(xml_dict, key_name: str):
    if xml_dict is None:
        return None
    try:
        for item in xml_dict["entry"]:
            if item is None:
                return None
            if item["key"] is not None and str(item["key"]).lower() == key_name.lower():
                return item["value"]
        return None
    except KeyError:
        return None
