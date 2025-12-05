import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.production.PartFactory import PartFactory
from models.production.Engine import Engine
from models.production.CarPart import CarPart
from config import constants


class TestPartFactory(unittest.TestCase):
    """Тесты для фабрики деталей"""

    def testCreateEngine(self):
        """Тест создания двигателя через фабрику"""
        engine = PartFactory.createPart(  # Исправлено на createPart
            "engine",
            partIdentifier="ENG001",
            partName="Тестовый двигатель",
            materialType="aluminum",
            partWeight=150.0,
            horsepower=300,
            cylinderCount=6,
            fuelType="gasoline"
        )
        self.assertIsInstance(engine, Engine)
        self.assertEqual(engine.partIdentifier, "ENG001")
        self.assertEqual(engine._horsepower, 300)

    def testCreateDemoEngine(self):
        """Тест создания демо-двигателя"""
        engine = PartFactory.createDemoEngine()  # Исправлено на createDemoEngine
        self.assertIsInstance(engine, Engine)
        self.assertEqual(engine.partIdentifier, "DEMO_ENG_001")
        self.assertEqual(engine._horsepower, constants.DEMO_ENGINE_HORSEPOWER)

    def testCreateCarPart(self):
        """Тест создания обычной детали автомобиля"""
        car_part = PartFactory.createPart(  # Исправлено на createPart
            "carPart",
            partIdentifier="PART001",
            partName="Тестовая деталь",
            materialType="steel",
            partWeight=10.5,
            partCategory="Test"
        )
        self.assertIsInstance(car_part, CarPart)
        self.assertEqual(car_part.partIdentifier, "PART001")
        self.assertEqual(car_part._partCategory, "Test")

    def testCreateUnknownPartType(self):
        """Тест на создание неизвестного типа детали"""
        with self.assertRaises(ValueError):
            PartFactory.createPart("unknown_type")  # Исправлено на createPart

    def testCreateDemoCarPart(self):
        """Тест создания демо-детали"""
        car_part = PartFactory.createDemoCarPart()  # Исправлено на createDemoCarPart
        self.assertIsInstance(car_part, CarPart)
        self.assertEqual(car_part.partIdentifier, "DEMO_PART_001")
        self.assertEqual(car_part._partCategory, "Standard")

    def testPartRegistry(self):
        """Тест регистрации типов деталей"""
        registry = PartFactory._partRegistry  # Исправлено на _partRegistry
        self.assertIn("engine", registry)
        self.assertIn("carPart", registry)
        self.assertIn("transmission", registry)
        self.assertIn("brakeSystem", registry)


if __name__ == '__main__':
    unittest.main()