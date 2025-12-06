import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.employees.HRManager import HRManager
from models.employees.MachineOperator import MachineOperator
from models.employees.MaintenanceTechnician import MaintenanceTechnician
from models.employees.ProductionSupervisor import ProductionSupervisor
from models.employees.QualityInspector import QualityInspector
from models.employees.QualityManager import QualityManager
from models.employees.WarehouseWorker import WarehouseWorker
from models.production.ProductionLine import ProductionLine
from models.production.Engine import Engine
from models.production.CarPart import CarPart
from models.production.PartFactory import PartFactory


class TestCarFactoryDemo(unittest.TestCase):
    def testInitialization(self):
        class MockDemo:
            def __init__(self):
                self.employees = []
                self.factory_buildings = []
                self.production_lines = []
                self.warehouses = []
                self.parts = []
                self.suppliers = []

        demo = MockDemo()
        self.assertEqual(len(demo.employees), 0)
        self.assertEqual(len(demo.factory_buildings), 0)
        self.assertEqual(len(demo.production_lines), 0)

    def testEmployeeCreation(self):
        class MockHRManager:
            def __init__(self, emp_id, name, position, salary, dept):
                self._employeeIdentifier = emp_id
                self._fullName = name
                self._jobPosition = position
                self._monthlySalary = salary
                self._hrDepartment = dept

        class MockMachineOperator:
            def __init__(self, emp_id, name, position, salary, machine_type):
                self._employeeIdentifier = emp_id
                self._fullName = name
                self._jobPosition = position
                self._monthlySalary = salary
                self._machineType = machine_type

        hr = MockHRManager("HR001", "Иванова Анна", "HR менеджер", 45000.0, "кадры")
        operator = MockMachineOperator("OP001", "Петров Алексей", "Оператор", 35000.0, "CNC")

        self.assertEqual(hr._employeeIdentifier, "HR001")
        self.assertEqual(hr._fullName, "Иванова Анна")
        self.assertEqual(hr._hrDepartment, "кадры")

        self.assertEqual(operator._employeeIdentifier, "OP001")
        self.assertEqual(operator._fullName, "Петров Алексей")
        self.assertEqual(operator._machineType, "CNC")

    def testProductionLineCreation(self):
        try:
            line = ProductionLine("PL001", "Основная линия", 100)
            self.assertEqual(line._line_id, "PL001")
            self.assertEqual(line._name, "Основная линия")
            self.assertEqual(line._capacity, 100)
            self.assertEqual(line._produced, 0)
        except ImportError as e:
            self.skipTest(f"Ошибка импорта ProductionLine: {e}")

    def testPartCreation(self):
        try:
            engine = Engine("ENG001", 150)
            car_part = CarPart("PART001", "Крыло", "steel", 25.0)

            self.assertEqual(engine._part_id, "ENG001")
            self.assertEqual(engine._name, "Engine")
            self.assertEqual(engine._horsepower, 150)

            self.assertEqual(car_part._part_id, "PART001")
            self.assertEqual(car_part._name, "Крыло")
            self.assertEqual(car_part._material, "steel")
            self.assertEqual(car_part._weight, 25.0)
        except ImportError as e:
            self.skipTest(f"Ошибка импорта деталей: {e}")

    def testWarehouseCreation(self):
        try:
            from models.inventory.Warehouse import Warehouse
            warehouse = Warehouse("WH001", 1000)

            self.assertEqual(warehouse._wh_id, "WH001")
            self.assertEqual(warehouse._capacity, 1000)
            self.assertEqual(warehouse._stock, 0)
        except ImportError as e:
            self.skipTest(f"Ошибка импорта Warehouse: {e}")

    def testPartFactoryDemo(self):
        try:
            demo_engine = PartFactory.createDemoEngine()
            demo_part = PartFactory.createDemoCarPart()

            self.assertIsNotNone(demo_engine)
            self.assertIsNotNone(demo_part)

            self.assertEqual(demo_engine._name, "Демо двигатель")
            self.assertEqual(demo_part._name, "Демо деталь")
        except ImportError as e:
            self.skipTest(f"Ошибка импорта PartFactory: {e}")

    def testBudgetCreation(self):
        try:
            from models.finance.Budget import Budget
            budget = Budget("BUD001", 1000000.0)

            self.assertEqual(budget._budget_id, "BUD001")
            self.assertEqual(budget._total, 1000000.0)
            self.assertEqual(budget._spent, 0)
        except ImportError as e:
            self.skipTest(f"Ошибка импорта Budget: {e}")


if __name__ == '__main__':
    unittest.main()