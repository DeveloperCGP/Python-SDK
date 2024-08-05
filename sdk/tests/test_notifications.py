import os

from ..adapters import notification_adapter


class TestXMLNotification:

    @staticmethod
    def read_xml_content(file_name):
        # Get the directory of the current file (test_notifications.py)
        current_file_directory = os.path.dirname(os.path.abspath(__file__))
        # Construct the path to the notifications directory relative to the current file
        xml_file_path = os.path.join(current_file_directory, 'notifications', file_name)

        if not os.path.exists(xml_file_path):
            raise FileNotFoundError(f"The file {xml_file_path} was not found.")

        with open(xml_file_path, 'r') as file:
            return file.read()

    def test_card_4907270002222227(self):
        xml_content = self.read_xml_content("4907270002222227.xml")
        notification = notification_adapter.parse_notification(xml_content)

        assert len(notification.operations) == 3, "Operation Size should be '3'"
        assert notification.operations[0].service == "TRA", "Service Name should be 'TRA'"
        assert notification.operations[0].status == "SUCCESS", "TRA Status should be 'SUCCESS'"

        assert notification.operations[1].service == "3DSv2", "Service Name should be '3DSv2'"
        assert notification.operations[1].status == "SUCCESS3DS", "ThreeDsService should be 'SUCCESS3DS'"

        assert notification.operations[-1].status == "SUCCESS", "PaymentSolution should be 'SUCCESS'"
        assert notification.status == "SUCCESS", "Transaction should be 'SUCCESS'"

    def test_card_4907271141151707(self):
        xml_content = self.read_xml_content("4907271141151707.xml")
        notification = notification_adapter.parse_notification(xml_content)

        assert len(notification.operations) == 3, "Operation Size should be '3'"
        assert notification.operations[0].service == "TRA", "Service Name should be 'TRA'"
        assert notification.operations[0].status == "SUCCESS", "TRA Status should be 'SUCCESS'"

        assert notification.operations[1].service == "3DSv2", "Service Name should be '3DSv2'"
        assert notification.operations[1].status == "SUCCESS3DS", "ThreeDsService should be 'SUCCESS3DS'"

        assert notification.operations[-1].status == "ERROR", "PaymentSolution should be 'ERROR'"
        assert notification.status == "SUCCESS", "Transaction should be 'SUCCESS'"

    def test_card_4907271141151715(self):
        xml_content = self.read_xml_content("4907271141151715.xml")
        notification = notification_adapter.parse_notification(xml_content)

        assert len(notification.operations) == 3, "Operation Size should be '3'"
        assert notification.operations[0].service == "TRA", "Service Name should be 'TRA'"
        assert notification.operations[0].status == "SUCCESS", "TRA Status should be 'SUCCESS'"

        assert notification.operations[1].service == "3DSv2", "Service Name should be '3DSv2'"
        assert notification.operations[1].status == "SUCCESS3DS", "ThreeDsService should be 'SUCCESS3DS'"

        assert notification.operations[-1].status == "ERROR", "PaymentSolution should be 'ERROR'"
        assert notification.status == "SUCCESS", "Transaction should be 'SUCCESS'"

    def test_card_4012000000010080(self):
        xml_content = self.read_xml_content("4012000000010080.xml")
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
        xml_content = self.read_xml_content("4012000000160083.xml")
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
        xml_content = self.read_xml_content("4012000000000081.xml")
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
        xml_content = self.read_xml_content("4012000000150084.xml")
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
        xml_content = self.read_xml_content("4907271141151723.xml")
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
        json_content = self.read_xml_content("xml_inside_json.json")
        notification = notification_adapter.parse_notification(json_content)
        assert notification.get_nemuru_cart_hash() == "898a0370-249b-43db-b604-e4ce5e7f120f", \
            "NemuruCartHash should be '898a0370-249b-43db-b604-e4ce5e7f120f'"
        assert notification.get_nemuru_auth_token() == "LHb76UKXmwW78LUI9VCWnwP9NKv5Qljt", \
            "NemuruAuthToken should be 'LHb76UKXmwW78LUI9VCWnwP9NKv5Qljt'"
