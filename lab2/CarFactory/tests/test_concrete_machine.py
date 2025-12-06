import unittest
from models.abstract.BaseMachine import BaseMachine


class ConcreteMachine(BaseMachine):
    def operate(self) -> bool:
        return True

    def calculate_efficiency(self) -> float:
        return 0.85


class TestConcreteMachine(unittest.TestCase):

    def testConcreteMachineInitialization(self):
        machine = ConcreteMachine("M001", "Станок ЧПУ", "CNC")
        self.assertEqual(machine._machine_id, "M001")
        self.assertEqual(machine._name, "Станок ЧПУ")
        self.assertEqual(machine._machine_type, "CNC")
        self.assertTrue(machine._is_active)

    def testConcreteMachineOperate(self):
        machine = ConcreteMachine("M001", "Станок ЧПУ", "CNC")
        result = machine.operate()
        self.assertTrue(result)

    def testConcreteMachineCalculateEfficiency(self):
        machine = ConcreteMachine("M001", "Станок ЧПУ", "CNC")
        efficiency = machine.calculate_efficiency()
        self.assertEqual(efficiency, 0.85)

    def testConcreteMachineProperties(self):
        machine = ConcreteMachine("M001", "Станок ЧПУ", "CNC")
        self.assertTrue(hasattr(machine, '_machine_id'))
        self.assertTrue(hasattr(machine, '_name'))
        self.assertTrue(hasattr(machine, '_machine_type'))
        self.assertTrue(hasattr(machine, '_is_active'))

    def testConcreteMachineScheduleMaintenance(self):
        machine = ConcreteMachine("M001", "Станок ЧПУ", "CNC")
        try:
            machine.schedule_maintenance()
            self.fail("Должно было выбросить исключение")
        except Exception as e:
            self.assertIn("MachineMaintenanceRequiredError", str(type(e).__name__))


if __name__ == '__main__':
    unittest.main()