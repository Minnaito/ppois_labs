import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.employees.MachineOperator import MachineOperator

class TestMachineOperator(unittest.TestCase):
    """Тесты для оператора станка"""

    def setUp(self):
        self.operator = MachineOperator("OP001", "Петр Петров", "Оператор", 35000.0, "CNC")

    def testOperatorInitialization(self):
        self.assertEqual(self.operator._machineType, "CNC")
        self.assertEqual(self.operator.employeeIdentifier, "OP001")

    def testPerformWorkDuties(self):
        duties = self.operator.performWorkDuties()
        self.assertIn("Оператор станка", duties)

    def testGetOperatorStats(self):
        stats = self.operator.getOperatorStats()
        self.assertEqual(stats["operatorId"], "OP001")
        self.assertEqual(stats["machineType"], "CNC")

if __name__ == '__main__':
    unittest.main()