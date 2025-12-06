import unittest
from models.employees.HRManager import HRManager
from models.employees.MachineOperator import MachineOperator
from models.employees.MaintenanceTechnician import MaintenanceTechnician
from models.employees.ProductionSupervisor import ProductionSupervisor
from models.employees.QualityInspector import QualityInspector
from models.employees.WarehouseWorker import WarehouseWorker


class TestAllEmployees(unittest.TestCase):

    def testAllEmployeeTypes(self):
        employees = [
            HRManager("HR001", "Анна", "HR менеджер", 45000.0, "кадры"),
            MachineOperator("OP001", "Алексей", "Оператор", 35000.0, "CNC"),
            MaintenanceTechnician("MT001", "Дмитрий", "Техник", 42000.0, "оборудование"),
            ProductionSupervisor("PS001", "Сергей", "Мастер", 55000.0, "сборочный"),
            QualityInspector("QI001", "Мария", "Инспектор", 38000.0, "ОТК"),
            WarehouseWorker("WW001", "Иван", "Кладовщик", 32000.0, "зона А")
        ]

        self.assertEqual(len(employees), 6)

        for emp in employees:
            work = emp.work()  # Используем work(), а не performWorkDuties()
            self.assertIsInstance(work, str)
            self.assertGreater(len(work), 0)


if __name__ == '__main__':
    unittest.main()