import unittest
from unittest.mock import patch, MagicMock
from config import constants
from models.abstract.BaseMachine import BaseMachine


class TestBaseMachine(unittest.TestCase):

    def testBaseMachineInitialization(self):
        """Тест инициализации базовой машины"""
        with patch.object(BaseMachine, '__abstractmethods__', set()):
            machine = BaseMachine("M001", "Токарный станок", "CNC")
            self.assertEqual(machine._machine_id, "M001")
            self.assertEqual(machine._name, "Токарный станок")
            self.assertEqual(machine._machine_type, "CNC")
            self.assertTrue(machine._is_active)

    def testScheduleMaintenance(self):
        """Тест планирования обслуживания"""
        with patch.object(BaseMachine, '__abstractmethods__', set()):
            machine = BaseMachine("M001", "Токарный станок", "CNC")

            # Импортируем здесь, чтобы избежать циклического импорта
            from exceptions.ProductionExceptions.MachineMaintenanceRequiredError import MachineMaintenanceRequiredError

            with self.assertRaises(MachineMaintenanceRequiredError) as context:
                machine.schedule_maintenance()

            exception = context.exception
            self.assertEqual(exception.machine_id, "M001")
            self.assertEqual(exception.maintenance_type, "плановое")


class TestConcreteMachine(unittest.TestCase):
    """Тест конкретной реализации машины"""

    class ConcreteMachine(BaseMachine):
        def operate(self) -> bool:
            return True

        def calculate_efficiency(self) -> float:
            return 85.5

    def testConcreteMachineOperate(self):
        """Тест работы конкретной машины"""
        machine = self.ConcreteMachine("CM001", "Фрезерный станок", "MILLING")
        result = machine.operate()
        self.assertTrue(result)

    def testConcreteMachineEfficiency(self):
        """Тест расчета эффективности"""
        machine = self.ConcreteMachine("CM001", "Фрезерный станок", "MILLING")
        efficiency = machine.calculate_efficiency()
        self.assertEqual(efficiency, 85.5)

    def testConcreteMachineProperties(self):
        """Тест свойств конкретной машины"""
        machine = self.ConcreteMachine("CM001", "Фрезерный станок", "MILLING")
        self.assertEqual(machine._machine_id, "CM001")
        self.assertEqual(machine._name, "Фрезерный станок")
        self.assertEqual(machine._machine_type, "MILLING")


if __name__ == '__main__':
    unittest.main()