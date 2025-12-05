import unittest
import sys
import os
from unittest.mock import Mock
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.quality.DefectReport import DefectReport
from models.production.CarPart import CarPart
from models.employees.QualityInspector import QualityInspector


class test_defect_report(unittest.TestCase):
    """Тесты для класса DefectReport"""

    def setUp(self):
        # Создаем мок-объекты для зависимостей
        self.mock_part = Mock(spec=CarPart)
        self.mock_part.partIdentifier = "PART001"
        self.mock_part.partName = "Тестовая деталь"
        self.mock_part.getDefectList.return_value = []

        self.mock_inspector = Mock(spec=QualityInspector)
        self.mock_inspector.employeeIdentifier = "INSP001"

        self.defectReport = DefectReport("REP001", self.mock_part, self.mock_inspector)

    def testDefectReportInitialization(self):
        self.assertEqual(self.defectReport._reportId, "REP001")
        self.assertEqual(self.defectReport._defectivePart, self.mock_part)
        self.assertEqual(self.defectReport._inspector, self.mock_inspector)
        self.assertEqual(self.defectReport._defectSeverity, "MEDIUM")
        self.assertEqual(self.defectReport._correctiveAction, "")
        self.assertFalse(self.defectReport._isResolved)
        self.assertIsNone(self.defectReport._resolutionDate)

        # Проверяем, что дата установлена в формате YYYY-MM-DD
        self.assertIsNotNone(self.defectReport._reportDate)
        date_parts = self.defectReport._reportDate.split("-")
        self.assertEqual(len(date_parts), 3)
        self.assertEqual(len(date_parts[0]), 4)  # Год
        self.assertEqual(len(date_parts[1]), 2)  # Месяц
        self.assertEqual(len(date_parts[2]), 2)  # День

    def testAddDefectDetails(self):
        defect_description = "Глубокая царапина"
        severity = "HIGH"

        self.defectReport.addDefectDetails(defect_description, severity)

        # Проверяем, что метод addDefect был вызван у детали
        self.mock_part.addDefect.assert_called_once_with(defect_description)
        self.assertEqual(self.defectReport._defectSeverity, severity)

    def testAssignCorrectiveAction(self):
        action = "Замена детали"
        self.defectReport.assignCorrectiveAction(action)

        self.assertEqual(self.defectReport._correctiveAction, action)

    def testMarkAsResolved(self):
        self.defectReport.markAsResolved()

        self.assertTrue(self.defectReport._isResolved)
        self.assertIsNotNone(self.defectReport._resolutionDate)

        # Проверяем формат даты разрешения
        resolution_parts = self.defectReport._resolutionDate.split("-")
        self.assertEqual(len(resolution_parts), 3)
        self.assertEqual(len(resolution_parts[0]), 4)
        self.assertEqual(len(resolution_parts[1]), 2)
        self.assertEqual(len(resolution_parts[2]), 2)

    def testCalculateRepairCostLowSeverity(self):
        self.defectReport._defectSeverity = "LOW"
        cost = self.defectReport.calculateRepairCost()

        self.assertEqual(cost, 50.0)  # 50.0 * 1.0

    def testCalculateRepairCostMediumSeverity(self):
        self.defectReport._defectSeverity = "MEDIUM"
        cost = self.defectReport.calculateRepairCost()

        self.assertEqual(cost, 75.0)  # 50.0 * 1.5

    def testCalculateRepairCostHighSeverity(self):
        self.defectReport._defectSeverity = "HIGH"
        cost = self.defectReport.calculateRepairCost()

        self.assertEqual(cost, 100.0)

    def testCalculateRepairCostCriticalSeverity(self):
        self.defectReport._defectSeverity = "CRITICAL"
        cost = self.defectReport.calculateRepairCost()

        self.assertEqual(cost, 150.0)

    def testCalculateRepairCostUnknownSeverity(self):
        self.defectReport._defectSeverity = "UNKNOWN"
        cost = self.defectReport.calculateRepairCost()

        self.assertEqual(cost, 50.0)

    def testGetDefectStatistics(self):
        # Настраиваем мок для возврата списка дефектов
        self.mock_part.getDefectList.return_value = ["Царапина", "Скол"]

        statistics = self.defectReport.getDefectStatistics()

        self.assertEqual(statistics["defectCount"], 2)
        self.assertEqual(statistics["defectSeverity"], "MEDIUM")
        self.assertEqual(statistics["repairCostEstimate"], 75.0)  # MEDIUM = 50.0 * 1.5
        self.assertEqual(statistics["daysSinceReport"], 1)

    def testGenerateReportSummaryUnresolved(self):
        summary = self.defectReport.generateReportSummary()

        self.assertEqual(summary["reportId"], "REP001")
        self.assertEqual(summary["partIdentifier"], "PART001")
        self.assertEqual(summary["partName"], "Тестовая деталь")
        self.assertEqual(summary["inspectorId"], "INSP001")
        self.assertEqual(summary["defectSeverity"], "MEDIUM")
        self.assertEqual(summary["correctiveAction"], "")
        self.assertFalse(summary["isResolved"])
        self.assertIsNone(summary["resolutionDate"])
        self.assertIsNotNone(summary["reportDate"])

    def testGenerateReportSummaryResolved(self):
        self.defectReport.assignCorrectiveAction("Полировка")
        self.defectReport.markAsResolved()

        summary = self.defectReport.generateReportSummary()

        self.assertEqual(summary["correctiveAction"], "Полировка")
        self.assertTrue(summary["isResolved"])
        self.assertIsNotNone(summary["resolutionDate"])

    def testMultipleDefectDetails(self):
        defects = [
            ("Царапина", "LOW"),
            ("Глубокая царапина", "HIGH"),
            ("Скол", "MEDIUM")
        ]

        for description, severity in defects:
            self.defectReport.addDefectDetails(description, severity)

        # Проверяем, что все дефекты были добавлены к детали
        self.assertEqual(self.mock_part.addDefect.call_count, 3)
        # Проверяем, что установлена последняя серьезность
        self.assertEqual(self.defectReport._defectSeverity, "MEDIUM")

    def testWorkflowComplete(self):
        # Полный рабочий процесс: создание -> добавление дефекта -> назначение действия -> разрешение
        self.defectReport.addDefectDetails("Критический дефект", "CRITICAL")
        self.defectReport.assignCorrectiveAction("Полная замена")
        self.defectReport.markAsResolved()

        self.assertTrue(self.defectReport._isResolved)
        self.assertEqual(self.defectReport._defectSeverity, "CRITICAL")
        self.assertEqual(self.defectReport._correctiveAction, "Полная замена")
        self.assertIsNotNone(self.defectReport._resolutionDate)

        # Проверяем стоимость ремонта для критического дефекта
        cost = self.defectReport.calculateRepairCost()
        self.assertEqual(cost, 150.0)

    def testReportDateIsToday(self):
        today = datetime.now().strftime("%Y-%m-%d")
        self.assertEqual(self.defectReport._reportDate, today)


if __name__ == '__main__':
    unittest.main()