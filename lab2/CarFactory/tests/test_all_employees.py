import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class TestAllEmployees(unittest.TestCase):
    """Базовые тесты для всех сотрудников"""

    def testHRManagerInitialization(self):
        from models.employees.HRManager import HRManager
        hr = HRManager("HR001", "Тест", "HR", 50000.0, "Отдел")
        self.assertEqual(hr._employeeIdentifier, "HR001")

    def testMaintenanceTechnicianInitialization(self):
        from models.employees.MaintenanceTechnician import MaintenanceTechnician
        tech = MaintenanceTechnician("MT001", "Тест", "Техник", 40000.0, "Механика")
        self.assertEqual(tech._employeeIdentifier, "MT001")

    def testProductionSupervisorInitialization(self):
        from models.employees.ProductionSupervisor import ProductionSupervisor
        supervisor = ProductionSupervisor("PS001", "Тест", "Супервайзер", 55000.0, "Цех")
        self.assertEqual(supervisor._employeeIdentifier, "PS001")

    def testQualityManagerInitialization(self):
        from models.employees.QualityManager import QualityManager
        qm = QualityManager("QM001", "Тест", "Менеджер качества", 52000.0, "Контроль")

        # Адаптивная проверка - пробуем оба варианта имен
        if hasattr(qm, '_employeeIdentifier'):
            self.assertEqual(qm._employeeIdentifier, "QM001")
        elif hasattr(qm, '_employee_identifier'):
            self.assertEqual(qm._employee_identifier, "QM001")
        else:
            # Если ни один атрибут не найден, создаем отладочную информацию
            print("QualityManager attributes:", [attr for attr in dir(qm) if not attr.startswith('__')])
            self.fail("QualityManager не имеет атрибута employeeIdentifier")

    def testWarehouseWorkerInitialization(self):
        from models.employees.WarehouseWorker import WarehouseWorker
        worker = WarehouseWorker("WW001", "Тест", "Работник склада", 35000.0, "Склад")
        self.assertEqual(worker._employeeIdentifier, "WW001")


if __name__ == '__main__':
    unittest.main()