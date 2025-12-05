import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.production.SuspensionSystem import SuspensionSystem
from exceptions.QualityExceptions.QualityStandardViolationError import QualityStandardViolationError
from config import constants

class TestSuspensionSystem(unittest.TestCase):
    """Тесты для класса SuspensionSystem"""

    def setUp(self):
        self.suspensionSystem = SuspensionSystem("SUSP001", "Передняя подвеска", "steel", 25.5, "McPherson", 15.0)

    def testSuspensionSystemInitialization(self):
        self.assertEqual(self.suspensionSystem._partIdentifier, "SUSP001")
        self.assertEqual(self.suspensionSystem._partName, "Передняя подвеска")
        self.assertEqual(self.suspensionSystem._materialType, "steel")
        self.assertEqual(self.suspensionSystem._partWeight, 25.5)
        self.assertEqual(self.suspensionSystem._partCategory, "Suspension")
        self.assertEqual(self.suspensionSystem._suspensionType, "McPherson")
        self.assertEqual(self.suspensionSystem._springRate, 15.0)
        self.assertEqual(self.suspensionSystem._dampingForce, 0.0)
        self.assertEqual(self.suspensionSystem._travelLengthMm, 0.0)
        self.assertFalse(self.suspensionSystem._adjustableStiffness)

    def testProductionCostCalculation(self):
        cost = self.suspensionSystem.calculateProductionCost()
        self.assertGreater(cost, 0)
        self.assertIsInstance(cost, float)

    def testQualityCheckSuccess(self):
        result = self.suspensionSystem.performQualityCheck()
        self.assertTrue(result)

    def testQualityCheckZeroSpringRate(self):
        self.suspensionSystem._springRate = constants.ZERO_VALUE
        with self.assertRaises(QualityStandardViolationError):
            self.suspensionSystem.performQualityCheck()

    def testQualityCheckNegativeSpringRate(self):
        self.suspensionSystem._springRate = -5.0
        with self.assertRaises(QualityStandardViolationError):
            self.suspensionSystem.performQualityCheck()

    def testCalculateComfortIndex(self):
        comfort_index = self.suspensionSystem.calculateComfortIndex()
        expected_comfort = 100 / (15.0 + 1)  # 100 / (springRate + 1)
        self.assertEqual(comfort_index, expected_comfort)
        self.assertIsInstance(comfort_index, float)

    def testSetDampingForce(self):
        new_damping_force = 120.5
        self.suspensionSystem.setDampingForce(new_damping_force)
        self.assertEqual(self.suspensionSystem._dampingForce, new_damping_force)

    def testAdjustStiffnessNotAdjustable(self):
        # Подвеска не регулируемая по умолчанию
        result = self.suspensionSystem.adjustStiffness(5)
        self.assertFalse(result)
        self.assertEqual(self.suspensionSystem._springRate, 15.0)

    def testAdjustStiffnessSuccess(self):
        self.suspensionSystem._adjustableStiffness = True
        result = self.suspensionSystem.adjustStiffness(5)
        self.assertTrue(result)
        self.assertEqual(self.suspensionSystem._springRate, 15.0)

    def testGetSuspensionSpecifications(self):
        self.suspensionSystem.setDampingForce(100.0)
        self.suspensionSystem._travelLengthMm = 150.0
        self.suspensionSystem._adjustableStiffness = True

        specs = self.suspensionSystem.getSuspensionSpecifications()

        self.assertEqual(specs["suspensionType"], "McPherson")
        self.assertEqual(specs["springRate"], 15.0)
        self.assertEqual(specs["dampingForce"], 100.0)
        self.assertEqual(specs["travelLengthMm"], 150.0)
        self.assertEqual(specs["comfortIndex"], 100 / (15.0 + 1))
        self.assertTrue(specs["adjustableStiffness"])

if __name__ == '__main__':
    unittest.main()