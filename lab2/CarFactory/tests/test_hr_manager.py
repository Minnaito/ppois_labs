import unittest
from models.employees.HRManager import HRManager
from models.abstract.BaseEmployee import BaseEmployee


class TestHRManager(unittest.TestCase):
    def testHRManagerInitialization(self):
        hr = HRManager("HR001", "Иванова Анна", "HR менеджер", 45000.0, "кадры")
        self.assertEqual(hr._employeeIdentifier, "HR001")
        self.assertEqual(hr._fullName, "Иванова Анна")
        self.assertEqual(hr._jobPosition, "HR менеджер")
        self.assertEqual(hr._monthlySalary, 45000.0)
        self.assertEqual(hr._hrDepartment, "кадры")

    def testHRManagerMethodsExistence(self):
        hr = HRManager("HR001", "Иванова Анна", "HR менеджер", 45000.0, "кадры")
        self.assertTrue(hasattr(hr, 'work'))
        self.assertTrue(hasattr(hr, 'process_payroll'))
        self.assertTrue(callable(hr.work))
        self.assertTrue(callable(hr.process_payroll))

    def testHRManagerInheritance(self):
        self.assertTrue(issubclass(HRManager, BaseEmployee))

    def testHRManagerWork(self):
        hr = HRManager("HR001", "Иванова Анна", "HR менеджер", 45000.0, "кадры")
        result = hr.work()
        self.assertEqual(result, "Управление персоналом в отделе кадры")

    def testHRManagerProcessPayroll(self):
        hr = HRManager("HR001", "Иванова Анна", "HR менеджер", 45000.0, "кадры")

        class MockEmployee:
            def __init__(self, salary):
                self._monthlySalary = salary

        employees = [MockEmployee(30000.0), MockEmployee(40000.0)]
        payroll = hr.process_payroll(employees)

        self.assertEqual(payroll["processed_by"], "HR001")
        self.assertEqual(payroll["employees_count"], 2)
        self.assertEqual(payroll["total_salary"], 70000.0)
        self.assertIn("date", payroll)


if __name__ == '__main__':
    unittest.main()