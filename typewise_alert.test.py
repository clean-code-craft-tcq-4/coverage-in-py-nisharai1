import unittest
from src import typewise_alert


class typeWiseTest(unittest.TestCase):
    def test_infers_breach_limits(self):
        self.assertTrue(typewise_alert.infer_breach(0, 0, 35) == 'NORMAL')
        self.assertTrue(typewise_alert.infer_breach(35, 0, 35) == 'NORMAL')
        self.assertTrue(typewise_alert.infer_breach(1, 0, 35) == 'NORMAL')
        self.assertTrue(typewise_alert.infer_breach(34, 0, 35) == 'NORMAL')
        self.assertTrue(typewise_alert.infer_breach(36, 0, 35) == 'TOO_HIGH')
        self.assertTrue(typewise_alert.infer_breach(-1, 0, 35) == 'TOO_LOW')

    def test_get_temperature(self):
        self.assertTrue(typewise_alert.definition.get_temperature('PASSIVE_COOLING') == (0, 35))
        self.assertTrue(typewise_alert.definition.get_temperature('MED_ACTIVE_COOLING') == (0, 40))
        self.assertTrue(typewise_alert.definition.get_temperature('HI_ACTIVE_COOLING') == (0, 45))
        self.assertFalse(typewise_alert.definition.get_temperature('PASSIVE_COOLING')[0] == -1)
        self.assertFalse(typewise_alert.definition.get_temperature('NORMAL_ACTIVE_COOLING')[1] == 41)
        self.assertFalse(typewise_alert.definition.get_temperature('HI_ACTIVE_COOLING')[1] == 46)
        self.assertFalse(typewise_alert.definition.get_temperature('PASSIVE_COOLING')[1] == 36)
        self.assertTrue(typewise_alert.definition.get_temperature('Invalid') is None)
        self.assertTrue('HI_ACTIVE_COOLING' in typewise_alert.definition.coolingType)
        self.assertFalse('Invalid' in typewise_alert.definition.coolingType)

    def test_get_step(self):
        self.assertTrue(typewise_alert.step.get_step('TO_CONTROLLER', 'TOO_LOW') == 0)
        self.assertTrue(typewise_alert.step.get_step('TO_EMAIL', 'TOO_HIGH') == 1)
        self.assertFalse('Invalid' in dict(typewise_alert.step.Config.targetType))
        self.assertEqual(typewise_alert.step.get_step('Invalid', 'TOO_LOW'), None)

    def test_send_to_email(self):
        self.assertFalse('Invalid' in typewise_alert.step.Config.breachType)
        self.assertTrue(typewise_alert.step.send_to_email('TOO_LOW')[0] == "a.b@c.com")
        self.assertFalse(typewise_alert.step.send_to_email('TOO_HIGH')[0] == "x.y@z.com")
        self.assertEqual(typewise_alert.step.send_to_email('TOO_LOW')[1],
                         "To: a.b@c.com" + '\n' + 'Hi, the temperature is too low')
        self.assertTrue(typewise_alert.step.send_to_email('TOO_HIGH')[
                            1] == "To: a.b@c.com" + '\n' + 'Hi, the temperature is too high')
        self.assertTrue(typewise_alert.step.send_to_email('Invalid') is None)
        self.assertTrue(typewise_alert.step.send_to_email('NORMAL') is None)

    def test_check_and_alert(self):
        self.assertEqual(typewise_alert.check_and_alert('TO_CONTROLLER', 'HI_ACTIVE_COOLING', 50), 0)
        self.assertEqual(typewise_alert.check_and_alert('TO_EMAIL', 'PASSIVE_COOLING', 41), 1)
        self.assertEqual(typewise_alert.check_and_alert('TO_EMAIL', 'Invalid', 41), None)
        self.assertEqual(typewise_alert.check_and_alert('Invalid', 'MED_ACTIVE_COOLING', 30), None)

    def test_classify_temperature_breach(self):
        self.assertTrue(typewise_alert.classify_temperature_breach('HI_ACTIVE_COOLING', 50) == 'TOO_HIGH')
        self.assertEqual(typewise_alert.classify_temperature_breach('Invalid', 25), None)
        self.assertEqual(typewise_alert.classify_temperature_breach('MED_ACTIVE_COOLING', -1), 'TOO_LOW')

    def test_send_to_controller(self):
        self.assertEqual(typewise_alert.step.send_to_controller('TOO_HIGH')[1], '65261, TOO_HIGH')
        self.assertEqual(typewise_alert.step.send_to_controller('TOO_LOW')[1], '65261, TOO_LOW')
        self.assertEqual(typewise_alert.step.send_to_controller('TOO_LOW')[0], 65261)
        self.assertEqual(typewise_alert.step.send_to_controller('Invalid'), None)
        self.assertEqual(typewise_alert.step.send_to_controller('NORMAL'), None)
        self.assertFalse(typewise_alert.step.send_to_controller('TOO_HIGH')[0] == 65260)


if __name__ == '__main__':
    unittest.main()