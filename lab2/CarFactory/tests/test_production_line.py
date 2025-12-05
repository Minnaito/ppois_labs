import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.production.ProductionLine import ProductionLine
from models.production.CarPart import CarPart
from models.production.Engine import Engine
from models.production.PartFactory import PartFactory
from exceptions.ProductionExceptions.ProductionCapacityExceededError import ProductionCapacityExceededError


class TestProductionLine(unittest.TestCase):
    """Тесты для класса ProductionLine"""

    def setUp(self):
        self.productionLine = ProductionLine("LINE001", "Тестовая линия", 100)
        self.testPart = CarPart("PART001", "Тестовая деталь", "steel", 5.0, "Test")

    def testProductionLineInitialization(self):
        self.assertEqual(self.productionLine._lineIdentifier, "LINE001")
        self.assertEqual(self.productionLine._lineName, "Тестовая линия")
        self.assertEqual(self.productionLine._maximumCapacity, 100)
        self.assertEqual(self.productionLine._currentProductionCount, 0)
        self.assertEqual(self.productionLine._assignedOperators, [])
        self.assertFalse(self.productionLine._isProductionActive)

    def testStartProductionLine(self):
        result = self.productionLine.startProductionLine()
        self.assertTrue(self.productionLine._isProductionActive)
        self.assertIn("Линия Тестовая линия запущена", result)

    def testProduceParts(self):
        self.productionLine.startProductionLine()
        producedParts = self.productionLine.produceParts(self.testPart, 10)  # Исправлено
        self.assertEqual(len(producedParts), 10)
        self.assertEqual(self.productionLine._currentProductionCount, 10)

    def testProducePartsWithoutStarting(self):
        with self.assertRaises(Exception) as context:
            self.productionLine.produceParts(self.testPart, 10)
        self.assertIn("Производственная линия не активна", str(context.exception))

    def testProductionCapacityExceeded(self):
        self.productionLine.startProductionLine()
        with self.assertRaises(ProductionCapacityExceededError):
            self.productionLine.produceParts(self.testPart, 150)

    def testProductionAtCapacityLimit(self):
        self.productionLine.startProductionLine()
        producedParts = self.productionLine.produceParts(self.testPart, 100)  # Исправлено
        self.assertEqual(len(producedParts), 100)
        self.assertEqual(self.productionLine._currentProductionCount, 100)

    def testStopProductionLine(self):
        self.productionLine.startProductionLine()
        result = self.productionLine.stopProductionLine()
        self.assertFalse(self.productionLine._isProductionActive)
        self.assertIn("Линия Тестовая линия остановлена", result)

    def testAddOperator(self):
        from models.employees.MachineOperator import MachineOperator
        operator = MachineOperator("OP001", "Петр Петров", "Оператор", 35000.0, "CNC")
        self.productionLine.addOperator(operator)
        self.assertIn(operator, self.productionLine._assignedOperators)

    def testGetProductionStatistics(self):
        stats = self.productionLine.getProductionStatistics()
        expectedStats = {  # Исправлено
            "lineIdentifier": "LINE001",
            "lineName": "Тестовая линия",
            "currentProduction": 0,
            "maximumCapacity": 100,
            "operatorCount": 0,
            "isActive": False
        }
        self.assertEqual(stats, expectedStats)

    def testMultipleProductionRuns(self):
        self.productionLine.startProductionLine()
        parts1 = self.productionLine.produceParts(self.testPart, 30)  # Исправлено
        parts2 = self.productionLine.produceParts(self.testPart, 40)  # Исправлено
        self.assertEqual(len(parts1), 30)
        self.assertEqual(len(parts2), 40)
        self.assertEqual(self.productionLine._currentProductionCount, 70)

    # Тесты для Part Factory
    def testCreateCarPart(self):
        """Тест создания обычной детали автомобиля"""
        carPart = PartFactory.createPart(  # Исправлено на createPart
            "carPart",
            partIdentifier="PART001",
            partName="Тестовая деталь",
            materialType="steel",
            partWeight=10.5,
            partCategory="Test"
        )
        self.assertIsInstance(carPart, CarPart)
        self.assertEqual(carPart.partIdentifier, "PART001")

    def testCreateDemoEngine(self):
        """Тест создания демо-двигателя"""
        engine = PartFactory.createDemoEngine()  # Исправлено на createDemoEngine
        self.assertIsInstance(engine, Engine)
        self.assertEqual(engine.partIdentifier, "DEMO_ENG_001")

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

    def testCreateUnknownPartType(self):
        """Тест на создание неизвестного типа детали"""
        with self.assertRaises(ValueError):
            PartFactory.createPart("unknown_type")  # Исправлено на createPart


if __name__ == '__main__':
    unittest.main()