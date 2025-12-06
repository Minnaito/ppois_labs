import unittest
from unittest.mock import patch, MagicMock
from models.employees.QualityInspector import QualityInspector
from models.abstract.BaseEmployee import BaseEmployee


class TestQualityInspector(unittest.TestCase):
    def setUp(self):
        class MockBaseEmployee(BaseEmployee):
            def __init__(self, employeeIdentifier, fullName, jobPosition, monthlySalary):
                self._employeeIdentifier = employeeIdentifier
                self._fullName = fullName
                self._jobPosition = jobPosition
                self._monthlySalary = monthlySalary

            def work(self):
                return "Mock work"

        patcher = patch('models.employees.QualityInspector.BaseEmployee', MockBaseEmployee)
        self.mock_base_employee = patcher.start()
        self.addCleanup(patcher.stop)

        self.inspector = QualityInspector(
            "QI001",
            "Сидорова Мария",
            "Инспектор качества",
            38000.0,
            "ОТК"
        )

    def testInitialization(self):
        self.assertEqual(self.inspector._employeeIdentifier, "QI001")
        self.assertEqual(self.inspector._fullName, "Сидорова Мария")
        self.assertEqual(self.inspector._jobPosition, "Инспектор качества")
        self.assertEqual(self.inspector._monthlySalary, 38000.0)
        self.assertEqual(self.inspector._departmentName, "ОТК")

    def testWork(self):
        work_result = self.inspector.work()
        expected_result = f"Проверка качества: {self.inspector._departmentName}"
        self.assertEqual(work_result, expected_result)

    def testInspectPart(self):
        result = self.inspector.inspect_part("PART001", True)

        self.assertEqual(result["inspector"], "QI001")
        self.assertEqual(result["part"], "PART001")
        self.assertTrue(result["passed"])

        result2 = self.inspector.inspect_part("PART002", False)
        self.assertFalse(result2["passed"])

    def testQualityInspectorProperties(self):
        self.assertTrue(hasattr(self.inspector, '_employeeIdentifier'))
        self.assertTrue(hasattr(self.inspector, '_fullName'))
        self.assertTrue(hasattr(self.inspector, '_jobPosition'))
        self.assertTrue(hasattr(self.inspector, '_monthlySalary'))
        self.assertTrue(hasattr(self.inspector, '_departmentName'))
        self.assertTrue(hasattr(self.inspector, 'work'))
        self.assertTrue(hasattr(self.inspector, 'inspect_part'))

    def testInheritance(self):
        self.assertTrue(issubclass(QualityInspector, BaseEmployee))


if __name__ == '__main__':
    unittest.main()