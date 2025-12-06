import unittest
from models.employees.MachineOperator import MachineOperator
from models.abstract.BaseEmployee import BaseEmployee


class TestMachineOperator(unittest.TestCase):
    def testMachineOperatorInitialization(self):
        operator = MachineOperator("OP001", "Петров Алексей", "Оператор", 35000.0, "CNC")
        self.assertEqual(operator._employeeIdentifier, "OP001")
        self.assertEqual(operator._fullName, "Петров Алексей")
        self.assertEqual(operator._jobPosition, "Оператор")
        self.assertEqual(operator._monthlySalary, 35000.0)
        self.assertEqual(operator._machineType, "CNC")

    def testMachineOperatorMethodsExistence(self):
        operator = MachineOperator("OP001", "Петров Алексей", "Оператор", 35000.0, "CNC")
        self.assertTrue(hasattr(operator, 'work'))
        self.assertTrue(hasattr(operator, 'operate_machine'))
        self.assertTrue(callable(operator.work))
        self.assertTrue(callable(operator.operate_machine))

    def testMachineOperatorInheritance(self):
        self.assertTrue(issubclass(MachineOperator, BaseEmployee))

    def testMachineOperatorWork(self):
        operator = MachineOperator("OP001", "Петров Алексей", "Оператор", 35000.0, "CNC")
        result = operator.work()
        self.assertEqual(result, "Оператор станка CNC")

    def testMachineOperatorOperateMachine(self):
        operator = MachineOperator("OP001", "Петров Алексей", "Оператор", 35000.0, "CNC")
        result = operator.operate_machine(10)

        self.assertEqual(result["operator"], "OP001")
        self.assertEqual(result["machine"], "CNC")
        self.assertEqual(result["parts_produced"], 10)


if __name__ == '__main__':
    unittest.main()