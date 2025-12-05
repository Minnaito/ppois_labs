import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.production.Engine import Engine
from exceptions.QualityExceptions.QualityStandardViolationError import QualityStandardViolationError
from config import constants

class TestEngine(unittest.TestCase):
    """Тесты для класса Engine"""

    def setUp(self):
        self.engine = Engine("ENG001", "V6 Engine", "aluminum", 150.0, 300, 6, "gasoline")

    def testEngineInitialization(self):
        self.assertEqual(self.engine._partIdentifier, "ENG001")
        self.assertEqual(self.engine._partName, "V6 Engine")
        self.assertEqual(self.engine._materialType, "aluminum")
        self.assertEqual(self.engine._partWeight, 150.0)
        self.assertEqual(self.engine._partCategory, "Engine")
        self.assertEqual(self.engine._horsepower, 300)
        self.assertEqual(self.engine._cylinderCount, 6)
        self.assertEqual(self.engine._fuelType, "gasoline")

    def testProductionCostCalculation(self):
        cost = self.engine.calculateProductionCost()
        self.assertGreater(cost, 0)
        self.assertIsInstance(cost, float)

    def testQualityCheckSuccess(self):
        result = self.engine.performQualityCheck()
        self.assertTrue(result)

    def testQualityCheckInvalidHorsepower(self):
        self.engine._horsepower = constants.MIN_ENGINE_HORSEPOWER - 10
        with self.assertRaises(QualityStandardViolationError):
            self.engine.performQualityCheck()

    def testQualityCheckInvalidCylinderCount(self):
        self.engine._cylinderCount = 3  # Невалидное количество цилиндров
        with self.assertRaises(QualityStandardViolationError):
            self.engine.performQualityCheck()

    def testCalculatePowerToWeightRatio(self):
        ratio = self.engine.calculatePowerToWeightRatio()
        expected_ratio = 300 / 150.0  # 2.0
        self.assertEqual(ratio, expected_ratio)

    def testGetEngineSpecifications(self):
        specs = self.engine.getEngineSpecifications()
        self.assertEqual(specs["partIdentifier"], "ENG001")
        self.assertEqual(specs["horsepower"], 300)
        self.assertEqual(specs["cylinderCount"], 6)
        self.assertEqual(specs["fuelType"], "gasoline")
        self.assertEqual(specs["powerToWeightRatio"], 2.0)

if __name__ == '__main__':
    unittest.main()