import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from unittest.mock import Mock
from models.production.CompositePart import CompositePart
from models.production.CarPart import CarPart


class TestCompositePart(unittest.TestCase):
    """Тесты для класса CompositePart"""

    def setUp(self):
        self.compositePart = CompositePart("COMP001", "Engine Block", "Aluminum", 50.0)
        self.mockChildPart = self._createMockChildPart()

    def _createMockChildPart(self):
        child = Mock(spec=CarPart)
        child.partIdentifier = "CHILD001"
        child._partWeight = 10.0
        child.calculateProductionCost.return_value = 100.0
        child.performQualityCheck.return_value = True
        child.getPartSpecifications.return_value = {
            "partIdentifier": "CHILD001",
            "partName": "Child Part",
            "materialType": "Steel",
            "partWeight": 10.0,
            "partCategory": "Component",
            "isQualityApproved": True,
            "defectCount": 0
        }
        return child

    def testCompositePartInitialization(self):
        self.assertEqual(self.compositePart._partIdentifier, "COMP001")
        self.assertEqual(self.compositePart._partName, "Engine Block")
        self.assertEqual(self.compositePart._materialType, "Aluminum")
        self.assertEqual(self.compositePart._partWeight, 50.0)
        self.assertEqual(self.compositePart._partCategory, "Composite")  # ← ПРОВЕРЯЕМ КАТЕГОРИЮ
        self.assertEqual(self.compositePart._childParts, [])
        self.assertEqual(self.compositePart._assemblyComplexity, 1.0)

    def testAddChildPart(self):
        self.compositePart.addChildPart(self.mockChildPart)
        self.assertEqual(len(self.compositePart._childParts), 1)
        self.assertEqual(self.compositePart._partWeight, 60.0)

    def testRemoveChildPartSuccess(self):
        self.compositePart.addChildPart(self.mockChildPart)
        result = self.compositePart.removeChildPart("CHILD001")
        self.assertTrue(result)
        self.assertEqual(len(self.compositePart._childParts), 0)
        self.assertEqual(self.compositePart._partWeight, 50.0)

    def testRemoveChildPartNotFound(self):
        result = self.compositePart.removeChildPart("NON_EXISTENT")
        self.assertFalse(result)

    def testCalculateProductionCostNoChildren(self):
        cost = self.compositePart.calculateProductionCost()
        self.assertIsInstance(cost, float)
        self.assertGreater(cost, 0)
        print(f"Cost without children: {cost}")  # Для отладки

    def testCalculateProductionCostWithChildren(self):
        self.compositePart.addChildPart(self.mockChildPart)
        cost = self.compositePart.calculateProductionCost()
        self.assertIsInstance(cost, float)
        self.assertGreater(cost, 0)
        print(f"Cost with children: {cost}")  # Для отладки

    def testPerformQualityCheckSuccess(self):
        result = self.compositePart.performQualityCheck()
        self.assertTrue(result)

    def testPerformQualityCheckWithChildren(self):
        self.compositePart.addChildPart(self.mockChildPart)
        result = self.compositePart.performQualityCheck()
        self.assertTrue(result)

    def testGetCompositeStructureNoChildren(self):
        structure = self.compositePart.getCompositeStructure()
        self.assertEqual(structure["compositeId"], "COMP001")
        self.assertEqual(structure["totalChildren"], 0)
        self.assertEqual(structure["totalWeight"], 50.0)
        self.assertEqual(structure["children"], [])

    def testGetCompositeStructureWithChildren(self):
        self.compositePart.addChildPart(self.mockChildPart)
        structure = self.compositePart.getCompositeStructure()
        self.assertEqual(structure["compositeId"], "COMP001")
        self.assertEqual(structure["totalChildren"], 1)
        self.assertEqual(structure["totalWeight"], 60.0)
        self.assertEqual(len(structure["children"]), 1)

    def testMultipleChildrenOperations(self):
        # Добавляем несколько деталей
        child1 = self._createMockChildPart()
        child2 = self._createMockChildPart()
        child2.partIdentifier = "CHILD002"
        child2._partWeight = 15.0

        self.compositePart.addChildPart(child1)
        self.compositePart.addChildPart(child2)

        self.assertEqual(len(self.compositePart._childParts), 2)
        self.assertEqual(self.compositePart._partWeight, 75.0)  # 50 + 10 + 15

        # Удаляем одну деталь
        result = self.compositePart.removeChildPart("CHILD001")
        self.assertTrue(result)
        self.assertEqual(len(self.compositePart._childParts), 1)
        self.assertEqual(self.compositePart._partWeight, 65.0)  # 50 + 15


if __name__ == '__main__':
    unittest.main()