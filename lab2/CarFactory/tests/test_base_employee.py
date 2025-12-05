import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.employees.MachineOperator import MachineOperator
from exceptions.EmployeeExceptions.InvalidEmployeeDataError import InvalidEmployeeDataError

class TestBaseEmployee(unittest.TestCase):
    """Тесты для базового сотрудника"""

    def test_employee_initialization(self):
        employee = MachineOperator("EMP001", "Иван Иванов", "Оператор", 30000.0, "CNC")
        self.assertEqual(employee.employeeIdentifier, "EMP001")

    def test_invalid_employee_data(self):
        with self.assertRaises(InvalidEmployeeDataError):
            MachineOperator("EMP002", "А", "Оператор", 30000.0, "CNC")

    def test_perform_work_duties(self):
        employee = MachineOperator("EMP003", "Петр Петров", "Оператор", 35000.0, "Фрезерный")
        duties = employee.performWorkDuties()
        self.assertIn("Оператор станка", duties)

if __name__ == '__main__':
    unittest.main()