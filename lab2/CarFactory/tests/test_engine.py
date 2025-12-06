import unittest
from models.production.Engine import Engine
from config import constants


class TestEngine(unittest.TestCase):
    def testEngineInitialization(self):
        engine = Engine("ENG001", 150)
        self.assertEqual(engine._part_id, "ENG001")
        self.assertEqual(engine._name, "Engine")
        self.assertEqual(engine._material, "steel")
        self.assertEqual(engine._weight, constants.DEMO_ENGINE_WEIGHT)
        self.assertEqual(engine._horsepower, 150)

    def testEngineCalculateCost(self):
        engine = Engine("ENG001", 150)
        cost = engine.calculate_cost()
        self.assertIsInstance(cost, float)
        self.assertGreater(cost, 0)

    def testEngineCalculateCostDifferentHorsepower(self):
        engine1 = Engine("ENG001", 100)
        engine2 = Engine("ENG002", 300)
        cost1 = engine1.calculate_cost()
        cost2 = engine2.calculate_cost()
        self.assertGreater(cost2, cost1)

    def testEngineCalculatePowerToWeight(self):
        engine = Engine("ENG001", 150)
        ratio = engine.calculate_power_to_weight()
        expected_ratio = 150 / constants.DEMO_ENGINE_WEIGHT
        self.assertEqual(ratio, expected_ratio)

    def testEngineCalculatePowerToWeightDifferentHorsepower(self):
        engine1 = Engine("ENG001", 100)
        engine2 = Engine("ENG002", 200)
        ratio1 = engine1.calculate_power_to_weight()
        ratio2 = engine2.calculate_power_to_weight()
        self.assertGreater(ratio2, ratio1)

    def testEngineCheckQuality(self):
        # Тестируем с мощностью >= 255 (300 * 0.85)
        engine = Engine("ENG001", 255)  # Граничное значение
        quality = engine.check_quality()
        self.assertTrue(quality)

        engine2 = Engine("ENG002", 300)  # Демо мощность
        quality2 = engine2.check_quality()
        self.assertTrue(quality2)

        engine3 = Engine("ENG003", 200)  # Ниже границы
        quality3 = engine3.check_quality()
        self.assertFalse(quality3)

    def testEngineCheckLowHorsepowerQuality(self):
        engine = Engine("ENG001", 50)
        quality = engine.check_quality()
        self.assertFalse(quality)

    def testEngineCheckHighHorsepowerQuality(self):
        engine = Engine("ENG001", 900)
        quality = engine.check_quality()
        # 900 >= 255, так что True
        self.assertTrue(quality)

    def testEngineShippingCost(self):
        engine = Engine("ENG001", 150)
        shipping_cost = engine.calculate_shipping_cost(100)
        expected_cost = constants.DEMO_ENGINE_WEIGHT * 100 * constants.SHIPPING_COST_PER_KG_PER_KM
        self.assertEqual(shipping_cost, expected_cost)

    def testEngineInheritance(self):
        from models.production.CarPart import CarPart
        self.assertTrue(issubclass(Engine, CarPart))


if __name__ == '__main__':
    unittest.main()