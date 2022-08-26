import unittest
import typewise_alert
from unittest.mock import patch


class TypewiseTest(unittest.TestCase):

    def setUp(self) -> None:
        self.recipient = "a.b@c.com"
        self.header = 0xfeed

    def test_infer_breach_normalPassive_cooling(self):
        self.assertTrue(typewise_alert.classify_temperature_breach("PASSIVE_COOLING", 25) == "NORMAL")

    def test_infer_breach_too_lowPassive_cooling(self):
        self.assertTrue(typewise_alert.classify_temperature_breach("PASSIVE_COOLING", -3) == "TOO_LOW")

    def test_infer_breach_too_highPassive_cooling(self):
        self.assertTrue(typewise_alert.classify_temperature_breach("PASSIVE_COOLING", 76) == "TOO_HIGH")

    def test_infer_breach_normalHI_ACTIVE_COOLING(self):
        self.assertTrue(typewise_alert.classify_temperature_breach("HI_ACTIVE_COOLING", 30) == "NORMAL")

    def test_infer_breach_too_lowHI_ACTIVE_COOLING(self):
        self.assertTrue(typewise_alert.classify_temperature_breach("HI_ACTIVE_COOLING", -2) == "TOO_LOW")

    def test_infer_breach_too_highHI_ACTIVE_COOLING(self):
        self.assertTrue(typewise_alert.classify_temperature_breach("HI_ACTIVE_COOLING", 49) == "TOO_HIGH")

    def test_infer_breach_normalMED_ACTIVE_COOLING(self):
        self.assertTrue(typewise_alert.classify_temperature_breach("MED_ACTIVE_COOLING", 38) == "NORMAL")

    def test_infer_breach_too_lowMED_ACTIVE_COOLING(self):
        self.assertTrue(typewise_alert.classify_temperature_breach("MED_ACTIVE_COOLING", -1) == "TOO_LOW")

    def test_infer_breach_too_highMED_ACTIVE_COOLING(self):
        self.assertTrue(typewise_alert.classify_temperature_breach("MED_ACTIVE_COOLING", 41) == "TOO_HIGH")

    def test_send_to_controllerLow(self):
        self.assertTrue(typewise_alert.send_to_controller('TOO_LOW') == "0xfeed, TOO_LOW")

    def test_send_to_controllerHigh(self):
        self.assertTrue(typewise_alert.send_to_controller('TOO_HIGH') == "0xfeed, TOO_HIGH")

    def test_send_to_emailLow(self):
        recepient_value, message = typewise_alert.send_to_email('TOO_LOW')
        self.assertTrue(recepient_value == "To: a.b@c.com")
        self.assertTrue(message == "Hi, the temperature is too low")

    def test_send_to_emailHigh(self):
        recepient_value, message = typewise_alert.send_to_email('TOO_HIGH')
        self.assertTrue(recepient_value == "To: a.b@c.com")
        self.assertTrue(message == "Hi, the temperature is too high")

    @patch('typewise_alert.send_to_controller')
    @patch('typewise_alert.send_to_email')
    def test_check_and_alert_positive_scenario(self, mock_send_to_email, mock_send_to_controller):
        batteryChar = {'coolingType': ''}
        typewise_alert.check_and_alert('TO_CONTROLLER', batteryChar, 0)
        mock_send_to_controller.assert_called_once()
        typewise_alert.check_and_alert('TO_EMAIL', batteryChar, 0)
        mock_send_to_email.assert_called_once()

    @patch('typewise_alert.send_to_controller')
    @patch('typewise_alert.send_to_email')
    def test_check_and_alert_with_negative_scenario(self, mock_send_to_email, mock_send_to_controller):
        batteryChar = {'coolingType': ''}
        typewise_alert.check_and_alert('', batteryChar, 0)
        mock_send_to_controller.assert_not_called()
        typewise_alert.check_and_alert('', batteryChar, 0)
        mock_send_to_email.assert_not_called()


if __name__ == '__main__':
    unittest.main()
