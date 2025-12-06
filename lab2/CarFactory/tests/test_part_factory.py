import unittest
from config import constants
from models.production.PartFactory import PartFactory
from models.production.Engine import Engine
from models.production.CarPart import CarPart


class TestPartFactory(unittest.TestCase):

    def testCreateEngine(self):
        """Тест создания двигателя через фабрику"""
        engine = PartFactory.createEngine("ENG001", "Двигатель V8")

        # Проверяем тип объекта
        self.assertIsInstance(engine, Engine)

        # Проверяем свойства
        self.assertEqual(engine._part_id, "ENG001")
        self.assertEqual(engine._name, "Двигатель V8")
        self.assertEqual(engine._horsepower, constants.DEMO_ENGINE_HORSEPOWER)
        self.assertEqual(engine._material, "steel")
        self.assertEqual(engine._weight, constants.DEMO_ENGINE_WEIGHT)

    def testCreateCarPart(self):
        """Тест создания детали через фабрику"""
        car_part = PartFactory.createCarPart("PART001", "Крыло")

        # Проверяем тип объекта
        self.assertIsInstance(car_part, CarPart)

        # Проверяем свойства
        self.assertEqual(car_part._part_id, "PART001")
        self.assertEqual(car_part._name, "Крыло")
        self.assertEqual(car_part._material, "steel")

        # Проверяем вес (демо-вес двигателя деленный на 10)
        expected_weight = constants.DEMO_ENGINE_WEIGHT / 10
        self.assertEqual(car_part._weight, expected_weight)

    def testCreateDemoEngine(self):
        """Тест создания демо-двигателя"""
        demo_engine = PartFactory.createDemoEngine()

        # Проверяем тип объекта
        self.assertIsInstance(demo_engine, Engine)

        # Проверяем стандартные демо-свойства
        self.assertEqual(demo_engine._part_id, "DEMO_ENG")
        self.assertEqual(demo_engine._name, "Демо двигатель")
        self.assertEqual(demo_engine._horsepower, constants.DEMO_ENGINE_HORSEPOWER)
        self.assertEqual(demo_engine._material, "steel")
        self.assertEqual(demo_engine._weight, constants.DEMO_ENGINE_WEIGHT)

    def testCreateDemoCarPart(self):
        """Тест создания демо-детали"""
        demo_part = PartFactory.createDemoCarPart()

        # Проверяем тип объекта
        self.assertIsInstance(demo_part, CarPart)

        # Проверяем стандартные демо-свойства
        self.assertEqual(demo_part._part_id, "DEMO_PART")
        self.assertEqual(demo_part._name, "Демо деталь")
        self.assertEqual(demo_part._material, "steel")

        expected_weight = constants.DEMO_ENGINE_WEIGHT / 10
        self.assertEqual(demo_part._weight, expected_weight)

    def testFactoryMethodsAreStatic(self):
        """Тест, что методы фабрики статические"""
        # Не создаем экземпляр фабрики, используем класс напрямую
        engine = PartFactory.createEngine("TEST", "Тест")
        self.assertIsInstance(engine, Engine)

        car_part = PartFactory.createCarPart("TEST", "Тест")
        self.assertIsInstance(car_part, CarPart)

        demo_engine = PartFactory.createDemoEngine()
        self.assertIsInstance(demo_engine, Engine)

        demo_part = PartFactory.createDemoCarPart()
        self.assertIsInstance(demo_part, CarPart)

    def testPartQuality(self):
        """Тест качества созданных деталей"""
        # Создаем детали
        engine = PartFactory.createEngine("ENG001", "Двигатель")
        car_part = PartFactory.createCarPart("PART001", "Деталь")
        demo_engine = PartFactory.createDemoEngine()
        demo_part = PartFactory.createDemoCarPart()

        # Проверяем качество всех деталей
        parts = [engine, car_part, demo_engine, demo_part]

        for part in parts:
            quality = part.check_quality()
            self.assertIsInstance(quality, bool)

    def testPartCostCalculation(self):
        """Тест расчета стоимости созданных деталей"""
        # Создаем детали
        engine = PartFactory.createEngine("ENG001", "Двигатель")
        car_part = PartFactory.createCarPart("PART001", "Деталь")

        # Рассчитываем стоимость
        engine_cost = engine.calculate_cost()
        car_part_cost = car_part.calculate_cost()

        # Проверяем, что стоимость положительная
        self.assertGreater(engine_cost, 0)
        self.assertGreater(car_part_cost, 0)


if __name__ == '__main__':
    unittest.main()