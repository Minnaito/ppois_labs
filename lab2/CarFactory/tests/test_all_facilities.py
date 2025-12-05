import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

class TestAllFacilities(unittest.TestCase):
    """Тесты для facilities с правильными сигнатурами"""

    def testFactoryBuildingInitialization(self):
        from models.facilities.FactoryBuilding import FactoryBuilding
        building = FactoryBuilding("FB001", "Завод", 10000, "Адрес", "Производственный")
        # Проверяем что объект создан
        self.assertTrue(building is not None)

    def testProductionHallInitialization(self):
        from models.facilities.ProductionHall import ProductionHall
        hall = ProductionHall("PH001", "Цех", 5000, "Здание А")
        self.assertTrue(hall is not None)

    def testSafetySystemInitialization(self):
        from models.facilities.SafetySystem import SafetySystem
        system = SafetySystem("SS001", "Система безопасности", "Пожарная")
        self.assertTrue(system is not None)

    def testStorageFacilityInitialization(self):
        from models.facilities.StorageFacility import StorageFacility
        facility = StorageFacility("SF001", "Склад", 2000, "Зона Б", True)
        self.assertTrue(facility is not None)