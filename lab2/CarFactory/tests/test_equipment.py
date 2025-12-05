import unittest
import sys
import os
from unittest.mock import Mock, patch

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# ИМПОРТ ИЗ ПРАВИЛЬНОГО ФАЙЛА
from models.quality.Equipment import Equipment


class TestingEquipmentTestCase(unittest.TestCase):
    """Юнит-тесты для испытательного оборудования"""

    def setUp(self):
        self.equipment = Equipment("EQ001", "Тестовое оборудование", "измерительное")

    def test_initialization(self):
        self.assertEqual(self.equipment._equipmentId, "EQ001")
        self.assertEqual(self.equipment._equipmentName, "Тестовое оборудование")
        self.assertEqual(self.equipment._equipmentType, "измерительное")
        self.assertTrue(self.equipment._isCalibrated)
        self.assertEqual(self.equipment._testsPerformed, 0)
        self.assertFalse(self.equipment._maintenanceRequired)

    def test_perform_test(self):
        test_result = self.equipment.performTest("PART001", {"parameter": "value"})

        self.assertEqual(test_result["equipmentId"], "EQ001")
        self.assertEqual(test_result["partIdentifier"], "PART001")
        self.assertTrue(test_result["testPassed"])
        self.assertEqual(self.equipment._testsPerformed, 1)

    def test_calibrate_equipment(self):
        self.equipment._isCalibrated = False
        self.equipment._maintenanceRequired = True

        self.equipment.calibrateEquipment()

        self.assertTrue(self.equipment._isCalibrated)
        self.assertFalse(self.equipment._maintenanceRequired)
        self.assertEqual(self.equipment._accuracyPercentage, 99.8)

    def test_schedule_maintenance(self):
        self.equipment.scheduleMaintenance()
        self.assertTrue(self.equipment._maintenanceRequired)

    def test_calculate_utilization_rate(self):
        self.equipment._testsPerformed = 50
        utilization = self.equipment.calculateUtilizationRate(100)
        self.assertEqual(utilization, 50.0)

    def test_calculate_utilization_rate_zero_available(self):
        utilization = self.equipment.calculateUtilizationRate(0)
        self.assertEqual(utilization, 0.0)

    def test_get_equipment_status(self):
        status = self.equipment.getEquipmentStatus()

        self.assertEqual(status["equipmentId"], "EQ001")
        self.assertEqual(status["equipmentName"], "Тестовое оборудование")
        self.assertEqual(status["equipmentType"], "измерительное")
        self.assertTrue(status["isCalibrated"])
        self.assertEqual(status["testsPerformed"], 0)
        self.assertFalse(status["maintenanceRequired"])


if __name__ == '__main__':
    unittest.main()