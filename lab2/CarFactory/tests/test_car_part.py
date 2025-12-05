import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.production.CarPart import CarPart
from exceptions.QualityExceptions.DefectivePartError import DefectivePartError

class TestCarPart(unittest.TestCase):
    """Тесты для класса CarPart"""

    def setUp(self):
        self.carPart = CarPart("TEST001", "Тестовая деталь", "steel", 10.5, "Test")

    def testCarPartInitialization(self):
        self.assertEqual(self.carPart.partIdentifier, "TEST001")
        self.assertEqual(self.carPart.partName, "Тестовая деталь")
        self.assertEqual(self.carPart._materialType, "steel")
        self.assertEqual(self.carPart._partWeight, 10.5)

    def testProductionCostCalculation(self):
        cost = self.carPart.calculateProductionCost()
        self.assertGreater(cost, 0)
        self.assertIsInstance(cost, float)
        # Проверим конкретные расчеты
        materialCost = len("steel") * 10  # MATERIAL_COST_MULTIPLIER
        complexityCost = len("Test") * 5  # COMPLEXITY_COST_MULTIPLIER
        weightCost = 10.5 * 2  # WEIGHT_COST_MULTIPLIER
        expectedCost = materialCost + complexityCost + weightCost
        self.assertEqual(cost, expectedCost)

    def testQualityCheck(self):
        result = self.carPart.performQualityCheck()
        self.assertTrue(result)

    def testQualityCheckWithDefects(self):
        self.carPart.addDefect("царапина")
        with self.assertRaises(DefectivePartError):
            self.carPart.performQualityCheck()

    def testAddDefect(self):
        self.carPart.addDefect("царапина")
        defects = self.carPart.getDefectList()
        self.assertEqual(len(defects), 1)
        self.assertIn("царапина", defects)
        self.assertFalse(self.carPart._isQualityApproved)

    def testApproveQuality(self):
        self.carPart.approveQuality()
        specs = self.carPart.getPartSpecifications()
        self.assertTrue(specs["isQualityApproved"])

    def testGetPartSpecifications(self):
        specs = self.carPart.getPartSpecifications()
        self.assertEqual(specs["partIdentifier"], "TEST001")
        self.assertEqual(specs["partName"], "Тестовая деталь")
        self.assertEqual(specs["materialType"], "steel")
        self.assertEqual(specs["partWeight"], 10.5)
        self.assertEqual(specs["partCategory"], "Test")

    def testMultipleDefects(self):
        self.carPart.addDefect("царапина")
        self.carPart.addDefect("скол")
        defects = self.carPart.getDefectList()
        self.assertEqual(len(defects), 2)
        self.assertIn("царапина", defects)
        self.assertIn("скол", defects)

    def testQualityApprovalResetsDefects(self):
        self.carPart.addDefect("царапина")
        self.carPart.approveQuality()
        # Одобрение не должно очищать дефекты, но должно менять статус
        self.assertTrue(self.carPart._isQualityApproved)
        self.assertEqual(len(self.carPart.getDefectList()), 1)

if __name__ == '__main__':
    unittest.main()