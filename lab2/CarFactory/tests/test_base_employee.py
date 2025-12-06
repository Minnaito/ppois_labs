import unittest
from models.abstract.BaseEmployee import BaseEmployee
from models.employees.HRManager import HRManager
from models.employees.MachineOperator import MachineOperator


class TestBaseEmployee(unittest.TestCase):
    def testBaseEmployeeInitialization(self):
        class TestEmployee(BaseEmployee):
            def work(self):
                return "test"

        emp = TestEmployee("EMP001", "Иван Иванов", "Оператор", 50000.0)
        self.assertEqual(emp._employeeIdentifier, "EMP001")
        self.assertEqual(emp._fullName, "Иван Иванов")
        self.assertEqual(emp._jobPosition, "Оператор")
        self.assertEqual(emp._monthlySalary, 50000.0)

    def testBaseEmployeeShortNameError(self):
        class TestEmployee(BaseEmployee):
            def work(self):
                return "test"

        try:
            TestEmployee("EMP001", "А", "Оператор", 50000.0)
            failed = False
        except ValueError as e:
            failed = True
            self.assertIn("Имя слишком короткое", str(e))
        self.assertTrue(failed, "Должно было выбросить ValueError для имени 'А'")

    def testBaseEmployeeLowSalaryError(self):
        class TestEmployee(BaseEmployee):
            def work(self):
                return "test"

        try:
            TestEmployee("EMP001", "Иван Иванов", "Оператор", 5000.0)
            failed = False
        except ValueError as e:
            failed = True
            self.assertIn("Зарплата ниже минимума", str(e))
        self.assertTrue(failed, "Должно было выбросить ValueError для зарплаты 5000")

    def testGetAnnualSalary(self):
        class TestEmployee(BaseEmployee):
            def work(self):
                return "test"

        emp = TestEmployee("EMP001", "Иван Иванов", "Оператор", 50000.0)
        self.assertEqual(emp.get_annual_salary(), 600000.0)

    def testCalculateTax(self):
        class TestEmployee(BaseEmployee):
            def work(self):
                return "test"

        emp = TestEmployee("EMP001", "Иван Иванов", "Оператор", 50000.0)
        tax = emp.calculate_tax()
        self.assertIsInstance(tax, float)
        self.assertGreater(tax, 0)


class TestHRManager(unittest.TestCase):
    def testHRManagerInitialization(self):
        hr = HRManager("HR001", "Анна Иванова", "HR менеджер", 45000.0, "кадры")
        self.assertEqual(hr._employeeIdentifier, "HR001")
        self.assertEqual(hr._fullName, "Анна Иванова")
        self.assertEqual(hr._jobPosition, "HR менеджер")
        self.assertEqual(hr._monthlySalary, 45000.0)
        self.assertEqual(hr._hrDepartment, "кадры")

    def testHRManagerWork(self):
        hr = HRManager("HR001", "Анна Иванова", "HR менеджер", 45000.0, "кадры")
        result = hr.work()
        self.assertIn("кадры", result)
        self.assertIn("Управление персоналом", result)


class TestMachineOperator(unittest.TestCase):
    def testMachineOperatorInitialization(self):
        operator = MachineOperator("OP001", "Петр Петров", "Оператор", 35000.0, "CNC")
        self.assertEqual(operator._employeeIdentifier, "OP001")
        self.assertEqual(operator._fullName, "Петр Петров")
        self.assertEqual(operator._jobPosition, "Оператор")
        self.assertEqual(operator._monthlySalary, 35000.0)
        self.assertEqual(operator._machineType, "CNC")

    def testMachineOperatorWork(self):
        operator = MachineOperator("OP001", "Петр Петров", "Оператор", 35000.0, "CNC")
        result = operator.work()
        self.assertIn("CNC", result)
        self.assertIn("Оператор станка", result)


if __name__ == '__main__':
    unittest.main()