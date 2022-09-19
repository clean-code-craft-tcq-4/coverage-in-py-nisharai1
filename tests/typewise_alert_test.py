import unittest
from src import typewise_alert


class typeWiseAlertTest(unittest.TestCase):
    def test_infers_breach_normal(self):
        self.assertTrue(typewise_alert.infer_breach(0, 0, 35) == 'NORMAL')
        self.assertTrue(typewise_alert.infer_breach(35, 0, 35) == 'NORMAL')
        self.assertTrue(typewise_alert.infer_breach(1, 0, 35) == 'NORMAL')
        self.assertFalse(typewise_alert.infer_breach(-1, 0, 35) == 'NORMAL')

    def test_infers_breach_high(self):
        self.assertTrue(typewise_alert.infer_breach(36, 0, 35) == 'TOO_HIGH')
        self.assertFalse(typewise_alert.infer_breach(0, 0, 36) == 'TOO_HIGH')
        self.assertFalse(typewise_alert.infer_breach(-1, 0, 36) == 'TOO_HIGH')

    def test_infers_breach_low(self):
        self.assertTrue(typewise_alert.infer_breach(-1, 0, 35) == 'TOO_L    OW')

    def test_get_temperature_passive_cooling(self):
        self.assertTrue(typewise_alert.definition.get_temperature('PASSIVE_COOLING') == (0, 35))
        self.assertFalse(typewise_alert.definition.get_temperature('PASSIVE_COOLING')[0] == -1)
        self.assertFalse(typewise_alert.definition.get_temperature('PASSIVE_COOLING')[1] == 36)

    def test_get_temperature_normal_active_cooling(self):
        self.assertTrue(typewise_alert.definition.get_temperature('NORMAL_ACTIVE_COOLING') == (0, 40))
        self.assertFalse(typewise_alert.definition.get_temperature('NORMAL_ACTIVE_COOLING')[1] == 41)
        self.assertFalse(typewise_alert.definition.get_temperature('NORMAL_ACTIVE_COOLING')[0] == -1)

    def test_get_temperature_hi_active_cooling(self):
        self.assertTrue(typewise_alert.definition.get_temperature('HI_ACTIVE_COOLING') == (0, 45))
        self.assertFalse(typewise_alert.definition.get_temperature('HI_ACTIVE_COOLING')[1] == 46)
        self.assertFalse(typewise_alert.definition.get_temperature('HI_ACTIVE_COOLING')[0] == -1)

    def test_get_step_positive_scenarios(self):
        self.assertTrue(typewise_alert.step.get_step('TO_CONTROLLER', 'TOO_LOW') == 0)
        self.assertTrue(typewise_alert.step.get_step('TO_EMAIL', 'TOO_HIGH') == 1)

    def test_get_step_negative_scenarios(self):
        self.assertFalse(typewise_alert.step.get_step('TO_CONTROLLER', 'TOO_LOW') == -1)
        self.assertFalse(typewise_alert.step.get_step('TO_EMAIL', 'TOO_HIGH') == 0)

    def test_send_to_email(self):
        self.assertEqual(typewise_alert.step.send_to_email('TOO_LOW')[1], "To: a.b@c.com" + '\t' + 'Hi, the '
                                                                                                   'temperature is '
                                                                                                   'too low')
        self.assertTrue(typewise_alert.step.send_to_email('TOO_HIGH')[1] == "To: a.b@c.com" + '\t' + 'Hi, the '
                                                                                                     'temperature is '
                                                                                                     'too high')
        self.assertFalse(typewise_alert.step.send_to_email('TOO_HIGH')[1] == "To: b.c@d.com" + '\t' + 'Hi, the '
                                                                                                      'temperature is '
                                                                                                      'too high')
        self.assertTrue(typewise_alert.step.send_to_email('TOO_LOW')[0] == "a.b@c.com")
        self.assertFalse(typewise_alert.step.send_to_email('TOO_HIGH')[0] == "b.c@d.com")

    def test_check_and_alert_to_controller(self):
        self.assertEqual(typewise_alert.check_and_alert('TO_CONTROLLER', 'HI_ACTIVE_COOLING', 46), 0)
        self.assertEqual(typewise_alert.check_and_alert('TO_CONTROLLER', 'PASSIVE_COOLING', 25), 0)
        self.assertEqual(typewise_alert.check_and_alert('TO_CONTROLLER', 'NORMAL_ACTIVE_COOLING', 30), 0)
        self.assertEqual(typewise_alert.check_and_alert('TO_CONTROLLER', 'Invalid', 35), None)

    def test_check_and_alert_to_email(self):
        self.assertEqual(typewise_alert.check_and_alert('TO_EMAIL', 'PASSIVE_COOLING', 32), 1)
        self.assertEqual(typewise_alert.check_and_alert('TO_EMAIL', 'HI_ACTIVE_COOLING', 47), 1)
        self.assertEqual(typewise_alert.check_and_alert('TO_EMAIL', 'NORMAL_ACTIVE_COOLING', 39), 1)
        self.assertEqual(typewise_alert.check_and_alert('TO_EMAIL', 'Invalid', 41), None)

    def test_classify_temperature_breach(self):
        self.assertFalse(typewise_alert.classify_temperature_breach('HI_ACTIVE_COOLING', 45) == 'TOO_HIGH')
        self.assertTrue(typewise_alert.classify_temperature_breach('HI_ACTIVE_COOLING', 47) == 'TOO_HIGH')
        self.assertEqual(typewise_alert.classify_temperature_breach('NORMAL_ACTIVE_COOLING', -1), 'TOO_LOW')

    def test_send_to_controller_high(self):
        self.assertEqual(typewise_alert.step.send_to_controller('TOO_HIGH')[1], '65261, TOO_HIGH')
        self.assertFalse(typewise_alert.step.send_to_controller('TOO_HIGH')[0] == 65260)

    def test_send_to_controller_low(self):
        self.assertEqual(typewise_alert.step.send_to_controller('TOO_LOW')[1], '65261, TOO_LOW')
        self.assertEqual(typewise_alert.step.send_to_controller('TOO_LOW')[0], 65261)


if __name__ == '__main__':
    unittest.main()
