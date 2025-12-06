import unittest
from models.production.CompositePart import CompositePart
from models.production.CarPart import CarPart


class TestCompositePart(unittest.TestCase):

    def testCompositePartInitialization(self):
        composite = CompositePart("COMP001", "Композитная деталь", "carbon", 25.0)

        self.assertIsInstance(composite, CompositePart)
        self.assertIsInstance(composite, CarPart)

        self.assertEqual(composite._part_id, "COMP001")
        self.assertEqual(composite._name, "Композитная деталь")
        self.assertEqual(composite._material, "carbon")
        self.assertEqual(composite._weight, 25.0)

        self.assertTrue(hasattr(composite, '_childParts'))

    def testAddChildPart(self):
        composite = CompositePart("COMP001", "Композитная деталь", "carbon", 25.0)

        self.assertTrue(hasattr(composite, 'addChild'))

        child_part = CarPart("CHILD001", "Дочерняя деталь", "steel", 5.0)
        result = composite.addChild(child_part)

        self.assertTrue(result)
        self.assertEqual(len(composite._childParts), 1)

    def testCalculateProductionCost(self):
        composite = CompositePart("COMP001", "Композитная деталь", "carbon", 25.0)

        self.assertTrue(hasattr(composite, 'calculateProductionCost'))

        child_part = CarPart("CHILD001", "Дочерняя деталь", "steel", 5.0)
        composite.addChild(child_part)

        cost = composite.calculateProductionCost()
        self.assertIsInstance(cost, (int, float))
        self.assertGreater(cost, 0)


if __name__ == '__main__':
    unittest.main()