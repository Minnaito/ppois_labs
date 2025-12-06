import unittest
from models.quality.Equipment import Equipment


class TestEquipment(unittest.TestCase):

    def setUp(self):
        self.equipment = Equipment("EQ001", "Микроскоп")

    def testInitialization(self):
        self.assertEqual(self.equipment._equip_id, "EQ001")
        self.assertEqual(self.equipment._name, "Микроскоп")
        self.assertTrue(self.equipment._is_calibrated)

    def testPerformTest(self):
        result = self.equipment.perform_test("PART001")
        self.assertTrue(result["passed"])
        self.assertEqual(result["equipment"], "Микроскоп")

    def testCalibrate(self):
        self.equipment._is_calibrated = False
        self.equipment.calibrate()
        self.assertTrue(self.equipment._is_calibrated)

    def testGetStatus(self):
        status = self.equipment.get_status()
        self.assertEqual(status["id"], "EQ001")
        self.assertTrue(status["calibrated"])


if __name__ == '__main__':
    unittest.main()