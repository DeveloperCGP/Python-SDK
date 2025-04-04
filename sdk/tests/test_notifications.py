import os
import unittest

from ..adapters import notification_adapter
from ..enums.currency import Currency


def read_file_content(file_name):
    # Get the directory of the current file (test_notifications.py)
    current_file_directory = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the notifications directory relative to the current file
    xml_file_path = os.path.join(current_file_directory, 'notifications', file_name)

    if not os.path.exists(xml_file_path):
        raise FileNotFoundError(f"The file {xml_file_path} was not found.")

    with open(xml_file_path, 'r') as file:
        return file.read()


class TestXMLNotification(unittest.TestCase):

    def test_card_4907270002222227(self):
        xml_content = read_file_content("4907270002222227.xml")
        notification = notification_adapter.parse_notification(xml_content)

        assert len(notification.operations) == 3, "Operation Size should be '3'"
        assert notification.operations[0].service == "TRA", "Service Name should be 'TRA'"
        assert notification.operations[0].status == "SUCCESS", "TRA Status should be 'SUCCESS'"

        assert notification.operations[1].service == "3DSv2", "Service Name should be '3DSv2'"
        assert notification.operations[1].status == "SUCCESS3DS", "ThreeDsService should be 'SUCCESS3DS'"

        assert notification.operations[-1].status == "SUCCESS", "PaymentSolution should be 'SUCCESS'"
        assert notification.status == "SUCCESS", "Transaction should be 'SUCCESS'"

    def test_card_4907271141151707(self):
        xml_content = read_file_content("4907271141151707.xml")
        notification = notification_adapter.parse_notification(xml_content)

        assert len(notification.operations) == 3, "Operation Size should be '3'"
        assert notification.operations[0].service == "TRA", "Service Name should be 'TRA'"
        assert notification.operations[0].status == "SUCCESS", "TRA Status should be 'SUCCESS'"

        assert notification.operations[1].service == "3DSv2", "Service Name should be '3DSv2'"
        assert notification.operations[1].status == "SUCCESS3DS", "ThreeDsService should be 'SUCCESS3DS'"

        assert notification.operations[-1].status == "ERROR", "PaymentSolution should be 'ERROR'"
        assert notification.status == "SUCCESS", "Transaction should be 'SUCCESS'"

    def test_card_4907271141151715(self):
        xml_content = read_file_content("4907271141151715.xml")
        notification = notification_adapter.parse_notification(xml_content)

        assert len(notification.operations) == 3, "Operation Size should be '3'"
        assert notification.operations[0].service == "TRA", "Service Name should be 'TRA'"
        assert notification.operations[0].status == "SUCCESS", "TRA Status should be 'SUCCESS'"

        assert notification.operations[1].service == "3DSv2", "Service Name should be '3DSv2'"
        assert notification.operations[1].status == "SUCCESS3DS", "ThreeDsService should be 'SUCCESS3DS'"

        assert notification.operations[-1].status == "ERROR", "PaymentSolution should be 'ERROR'"
        assert notification.status == "SUCCESS", "Transaction should be 'SUCCESS'"

    def test_card_4012000000010080(self):
        xml_content = read_file_content("4012000000010080.xml")
        notification = notification_adapter.parse_notification(xml_content)

        assert len(notification.operations) == 2, "Operation Size should be '2'"
        assert notification.operations[0].service == "TRA", "Service Name should be 'TRA'"
        assert notification.operations[0].status == "SUCCESS", "TRA Status should be 'SUCCESS'"

        assert notification.operations[1].service == "3DSv2", "Service Name should be '3DSv2'"
        assert notification.operations[1].status == "ERROR3DS", "ThreeDsService should be 'ERROR3DS'"
        assert notification.operations[
                   1].paymentMessage == "Not authenticated", "Payment message should be 'Not authenticated'"

        assert notification.operations[-1].paymentSolution is None, "PaymentSolution should be null"
        assert notification.status == "ERROR", "Transaction should be 'ERROR'"

    def test_card_4012000000160083(self):
        xml_content = read_file_content("4012000000160083.xml")
        notification = notification_adapter.parse_notification(xml_content)

        assert len(notification.operations) == 2, "Operation Size should be '2'"
        assert notification.operations[0].service == "TRA", "Service Name should be 'TRA'"
        assert notification.operations[0].status == "SUCCESS", "TRA Status should be 'SUCCESS'"

        assert notification.operations[1].service == "3DSv2", "Service Name should be '3DSv2'"
        assert notification.operations[1].status == "ERROR3DS", "ThreeDsService should be 'ERROR3DS'"
        assert notification.operations[1].paymentMessage == ("Not authenticated because the issuer is rejecting "
                                                             "authentication"), \
            "Payment message should be 'Not authenticated because the issuer is rejecting authentication'"

        assert notification.operations[-1].paymentSolution is None, "PaymentSolution should be null"
        assert notification.status == "ERROR", "Transaction should be 'ERROR'"

    def test_card_4012000000000081(self):
        xml_content = read_file_content("4012000000000081.xml")
        notification = notification_adapter.parse_notification(xml_content)

        assert len(notification.operations) == 2, "Operation Size should be '2'"
        assert notification.operations[0].service == "TRA", "Service Name should be 'TRA'"
        assert notification.operations[0].status == "SUCCESS", "TRA Status should be 'SUCCESS'"

        assert notification.operations[1].service == "3DSv2", "Service Name should be '3DSv2'"
        assert notification.operations[1].status == "ERROR3DS", "ThreeDsService should be 'ERROR3DS'"
        assert notification.operations[1].paymentMessage == "Not authenticated due to technical or other issue", \
            "Payment message should be 'Not authenticated due to technical or other issue'"

        assert notification.operations[-1].paymentSolution is None, "PaymentSolution should be null"
        assert notification.status == "ERROR", "Transaction should be 'ERROR'"

    def test_card_4012000000150084(self):
        xml_content = read_file_content("4012000000150084.xml")
        notification = notification_adapter.parse_notification(xml_content)

        assert len(notification.operations) == 3, "Operation Size should be '3'"
        assert notification.operations[0].service == "TRA", "Service Name should be 'TRA'"
        assert notification.operations[0].status == "SUCCESS", "TRA Status should be 'SUCCESS'"

        assert notification.operations[1].service == "3DSv2", "Service Name should be '3DSv2'"
        assert notification.operations[1].status == "SUCCESS3DS", "ThreeDsService should be 'SUCCESS3DS'"
        assert notification.operations[1].message == "Challenge: Authenticated successfully", \
            "ThreeDs Message should be 'Challenge: Authenticated successfully'"

        assert notification.operations[-1].status == "SUCCESS", "PaymentSolution should be 'SUCCESS'"
        assert notification.status == "SUCCESS", "Transaction should be 'SUCCESS'"

    def test_card_4907271141151723(self):
        xml_content = read_file_content("4907271141151723.xml")
        notification = notification_adapter.parse_notification(xml_content)

        assert len(notification.operations) == 3, "Operation Size should be '3'"
        assert notification.operations[0].service == "TRA", "Service Name should be 'TRA'"
        assert notification.operations[0].status == "SUCCESS", "TRA Status should be 'SUCCESS'"

        assert notification.operations[1].service == "3DSv2", "Service Name should be '3DSv2'"
        assert notification.operations[1].status == "SUCCESS3DS", "ThreeDsService should be 'SUCCESS3DS'"

        assert notification.operations[-1].status == "ERROR", "PaymentSolution should be 'ERROR'"
        assert notification.operations[-1].message == ("Denied 'Settle' operation with code: 180 message: "
                                                       "Tarjeta ajena al servicio o no compatible."), \
            ("ThreeDs Message should be 'Denied 'Settle' operation with code: 180 message: "
             "Tarjeta ajena al servicio o no compatible.'")
        assert notification.status == "SUCCESS", "Transaction should be 'SUCCESS'"

    def test_xml_inside_json(self):
        json_content = read_file_content("xml_inside_json.json")
        notification = notification_adapter.parse_notification(json_content)
        assert notification.get_nemuru_cart_hash() == "898a0370-249b-43db-b604-e4ce5e7f120f", \
            "NemuruCartHash should be '898a0370-249b-43db-b604-e4ce5e7f120f'"
        assert notification.get_nemuru_auth_token() == "LHb76UKXmwW78LUI9VCWnwP9NKv5Qljt", \
            "NemuruAuthToken should be 'LHb76UKXmwW78LUI9VCWnwP9NKv5Qljt'"
        
    def test_parsing_xml_notification(self):
        xml_content = read_file_content("sample_response/notification.xml")
        notification = notification_adapter.parse_notification(xml_content)

        self.assertEqual(3, len(notification.operations))

        self.assertEqual("TRA", notification.operations[0].service)
        self.assertEqual("SUCCESS", notification.operations[0].status)
        self.assertEqual(13.0, notification.operations[0].amount)
        self.assertEqual(Currency.EUR, notification.operations[0].currency)
        self.assertEqual("8203", notification.operations[0].respCode.code)
        self.assertEqual("Frictionless requires", notification.operations[0].respCode.message)
        self.assertEqual("1496918", notification.operations[0].merchantTransactionId)
        self.assertEqual("8232609", notification.operations[0].transactionId)

        self.assertEqual("3DSv2", notification.operations[1].service)
        self.assertEqual("SUCCESS3DS", notification.operations[1].status)
        self.assertEqual(13.0, notification.operations[1].amount)
        self.assertEqual(Currency.EUR, notification.operations[1].currency)
        self.assertEqual("1496918", notification.operations[1].merchantTransactionId)
        self.assertEqual("8232609", notification.operations[1].transactionId)
        self.assertEqual("nsY1", notification.operations[1].paymentCode)
        self.assertEqual("163c965a-9772-4bb1-a2f4-e96e184a2661", notification.operations[1].mpi.acsTransID)
        self.assertEqual("AJkBB4OBmVFmgYFYFIGZAAAAAAA=", notification.operations[1].mpi.cavv)

        self.assertEqual("SUCCESS", notification.operations[2].status)
        self.assertEqual("Success 'Settle' operation", notification.operations[2].message)
        self.assertEqual(13.0, notification.operations[2].amount)
        self.assertEqual(Currency.EUR, notification.operations[2].currency)
        self.assertEqual("8232609", notification.operations[2].transactionId)
        self.assertEqual("test", notification.operations[2].paymentDetails.cardHolderName)
        self.assertEqual("000", notification.operations[2].paymentCode)

        self.assertEqual("sdk", notification.operations[-1].optionalTransactionParams.entry[0].key)
        self.assertEqual("php", notification.operations[-1].optionalTransactionParams.entry[0].value)
        self.assertEqual("type", notification.operations[-1].optionalTransactionParams.entry[1].key)
        self.assertEqual("JsCharge", notification.operations[-1].optionalTransactionParams.entry[1].value)
        self.assertEqual("version", notification.operations[-1].optionalTransactionParams.entry[2].key)
        self.assertEqual("1.00", notification.operations[-1].optionalTransactionParams.entry[2].value)

        self.assertEqual("sdk", notification.optionalTransactionParams.entry[0].key)
        self.assertEqual("php", notification.optionalTransactionParams.entry[0].value)
        self.assertEqual("type", notification.optionalTransactionParams.entry[1].key)
        self.assertEqual("JsCharge", notification.optionalTransactionParams.entry[1].value)
        self.assertEqual("version", notification.optionalTransactionParams.entry[2].key)
        self.assertEqual("1.00", notification.optionalTransactionParams.entry[2].value)

        self.assertEqual("SUCCESS", notification.status)

    def test_parsing_json_notification(self):
        json_content = read_file_content("sample_response/notification.json")
        notification = notification_adapter.parse_notification(json_content)

        self.assertEqual(2, len(notification.operations))

        self.assertEqual("TRA", notification.operations[0].service)
        self.assertEqual("SUCCESS", notification.operations[0].status)
        self.assertEqual(30.0, notification.operations[0].amount)
        self.assertEqual(Currency.EUR, notification.operations[0].currency)
        self.assertEqual("8203", notification.operations[0].respCode.code)
        self.assertEqual("Frictionless requires", notification.operations[0].respCode.message)
        self.assertEqual("23506844", notification.operations[0].merchantTransactionId)

        self.assertEqual("3DSv2", notification.operations[1].service)
        self.assertEqual("REDIRECTED", notification.operations[1].status)
        self.assertEqual(30.0, notification.operations[1].amount)
        self.assertEqual(Currency.EUR, notification.operations[1].currency)
        self.assertEqual("threeDSMethodData", notification.operations[1].paymentDetails.extraDetails.entry[0].key)
        self.assertEqual(
            "eyJ0aHJlZURTU2VydmVyVHJhbnNJRCI6IjRhNzUwYmNlLWEwM2UtNGI1Ni1iMTRmLWE1YTBlNjc5YTRiOSIsICJ0aHJlZURTTWV0aG9kTm90aWZpY2F0aW9uVVJMIjogImh0dHBzOi8vY2hlY2tvdXQuc3RnLWV1LXdlc3QxLmVwZ2ludC5jb20vRVBHQ2hlY2tvdXQvY2FsbGJhY2svZ2F0aGVyRGV2aWNlTm90aWZpY2F0aW9uL3BheXNvbC8zZHN2Mi8xMTA4MTA0In0=",
            notification.operations[1].paymentDetails.extraDetails.entry[0].value
        )
        self.assertEqual("threeDSv2Token", notification.operations[1].paymentDetails.extraDetails.entry[1].key)
        self.assertEqual(
            "4a750bce-a03e-4b56-b14f-a5a0e679a4b9",
            notification.operations[1].paymentDetails.extraDetails.entry[1].value
        )
        self.assertEqual("sdk", notification.operations[1].optionalTransactionParams.entry[0].key)
        self.assertEqual("php", notification.operations[1].optionalTransactionParams.entry[0].value)
        self.assertEqual("type", notification.operations[1].optionalTransactionParams.entry[1].key)
        self.assertEqual("JsCharge", notification.operations[1].optionalTransactionParams.entry[1].value)
        self.assertEqual("version", notification.operations[1].optionalTransactionParams.entry[2].key)
        self.assertEqual("1.00", notification.operations[1].optionalTransactionParams.entry[2].value)

        self.assertEqual("ClaveN", notification.optionalTransactionParams.entry[0].key)
        self.assertEqual("ValorN", notification.optionalTransactionParams.entry[0].value)
        self.assertEqual("Clave1", notification.optionalTransactionParams.entry[1].key)
        self.assertEqual("Valor1", notification.optionalTransactionParams.entry[1].value)
        self.assertEqual("Clave2", notification.optionalTransactionParams.entry[2].key)
        self.assertEqual("Valor2", notification.optionalTransactionParams.entry[2].value)



