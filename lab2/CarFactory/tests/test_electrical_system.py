import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.production.ElectricalSystem import ElectricalSystem
from exceptions.QualityExceptions.QualityStandardViolationError import QualityStandardViolationError
from config import constants

class TestElectricalSystem(unittest.TestCase):
    """Тесты для класса ElectricalSystem"""

    def setUp(self):
        self.electricalSystem = ElectricalSystem("ELEC001", "Main Wiring Harness", "Copper", 5.0, 12.0, 30.0)

    def testElectricalSystemInitialization(self):
        self.assertEqual(self.electricalSystem._partIdentifier, "ELEC001")
        self.assertEqual(self.electricalSystem._partName, "Main Wiring Harness")
        self.assertEqual(self.electricalSystem._materialType, "Copper")
        self.assertEqual(self.electricalSystem._partWeight, 5.0)
        self.assertEqual(self.electricalSystem._partCategory, "ElectricalSystem")
        self.assertEqual(self.electricalSystem._systemVoltage, 12.0)
        self.assertEqual(self.electricalSystem._currentRating, 30.0)
        self.assertEqual(self.electricalSystem._wireGauge, 2.5)
        self.assertEqual(self.electricalSystem._insulationType, "PVC")
        self.assertEqual(self.electricalSystem._batteryCapacity, 0.0)

    def testProductionCostCalculation(self):
        cost = self.electricalSystem.calculateProductionCost()
        self.assertGreater(cost, 0)
        self.assertIsInstance(cost, float)

    def testQualityCheckSuccess(self):
        result = self.electricalSystem.performQualityCheck()
        self.assertTrue(result)

    def testQualityCheckVoltageTooLow(self):
        self.electricalSystem._systemVoltage = constants.MIN_VOLTAGE - 1
        with self.assertRaises(QualityStandardViolationError):
            self.electricalSystem.performQualityCheck()

    def testQualityCheckVoltageTooHigh(self):
        self.electricalSystem._systemVoltage = constants.MAX_VOLTAGE + 1
        with self.assertRaises(QualityStandardViolationError):
            self.electricalSystem.performQualityCheck()

    def testCalculatePowerCapacity(self):
        power = self.electricalSystem.calculatePowerCapacity()
        expected_power = 12.0 * 30.0  # voltage * current
        self.assertEqual(power, expected_power)
        self.assertIsInstance(power, float)

    def testChangeInsulationType(self):
        new_insulation = "Silicone"
        self.electricalSystem.changeInsulationType(new_insulation)
        self.assertEqual(self.electricalSystem._insulationType, new_insulation)

    def testSetBatteryCapacity(self):
        battery_capacity = 60.0
        self.electricalSystem.setBatteryCapacity(battery_capacity)
        self.assertEqual(self.electricalSystem._batteryCapacity, battery_capacity)

    def testGetElectricalSpecifications(self):
        specs = self.electricalSystem.getElectricalSpecifications()
        self.assertEqual(specs["systemVoltage"], 12.0)
        self.assertEqual(specs["currentRating"], 30.0)
        self.assertEqual(specs["powerCapacity"], 360.0)
        self.assertEqual(specs["insulationType"], "PVC")
        self.assertEqual(specs["batteryCapacity"], 0.0)
        self.assertEqual(specs["wireGauge"], 2.5)

if __name__ == '__main__':
    unittest.main()