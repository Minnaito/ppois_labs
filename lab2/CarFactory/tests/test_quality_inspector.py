import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.employees.QualityInspector import QualityInspector
from models.production.CarPart import CarPart
from models.quality.QualityControl import QualityControl

class TestQualityInspector(unittest.TestCase):
    """Тесты для инспектора качества"""

    def setUp(self):
        self.inspector = QualityInspector("INS001", "Иван Петров", "Инспектор", 45000.0, "Производство")
        self.testPart = CarPart("PART001", "Тестовая деталь", "steel", 10.5, "Test")
        self.qualityControl = QualityControl("QC001", "Основной контроль")

    def test_inspector_initialization(self):
        self.assertEqual(self.inspector.employeeIdentifier, "INS001")
        self.assertEqual(self.inspector._departmentName, "Производство")

    def test_perform_work_duties(self):
        duties = self.inspector.performWorkDuties()
        self.assertIn("Проверка качества", duties)

    def test_inspect_part(self):
        result = self.inspector.inspectPart(self.testPart, self.qualityControl)
        self.assertTrue(result)

    def test_calculate_success_rate(self):
        successRate = self.inspector.calculateSuccessRate(10)
        self.assertGreaterEqual(successRate, 0)

if __name__ == '__main__':
    unittest.main()