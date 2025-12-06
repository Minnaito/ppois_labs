import unittest
from models.finance.FinancialReport import FinancialReport
from config import constants


class TestFinancialReport(unittest.TestCase):

    def testFinancialReportInitialization(self):
        """Тест инициализации финансового отчета"""
        report = FinancialReport("FR001", "Q1 2024")

        self.assertEqual(report._report_id, "FR001")
        self.assertEqual(report._period, "Q1 2024")

    def testFinancialReportGenerate(self):
        """Тест генерации отчета"""
        report = FinancialReport("FR001", "Q1 2024")

        revenue = 1500000
        expenses = 1000000

        result = report.generate(revenue, expenses)

        # Проверяем структуру результата
        self.assertEqual(result["report_id"], "FR001")
        self.assertEqual(result["period"], "Q1 2024")
        self.assertEqual(result["revenue"], revenue)
        self.assertEqual(result["expenses"], expenses)

        # Проверяем расчет прибыли
        expected_profit = revenue - expenses
        self.assertEqual(result["profit"], expected_profit)

        # Проверяем расчет маржи (может быть 0 для отрицательной выручки)
        self.assertIsInstance(result["margin"], (int, float))

    def testFinancialReportGenerateZeroRevenue(self):
        """Тест генерации отчета при нулевой выручке"""
        report = FinancialReport("FR001", "Q1 2024")

        result = report.generate(0, 500000)

        self.assertEqual(result["revenue"], 0)
        self.assertEqual(result["expenses"], 500000)
        self.assertEqual(result["profit"], -500000)

    def testFinancialReportGenerateZeroExpenses(self):
        """Тест генерации отчета при нулевых расходах"""
        report = FinancialReport("FR001", "Q1 2024")

        result = report.generate(1000000, 0)

        self.assertEqual(result["revenue"], 1000000)
        self.assertEqual(result["expenses"], 0)
        self.assertEqual(result["profit"], 1000000)

    def testFinancialReportGenerateBreakEven(self):
        """Тест генерации отчета в точке безубыточности"""
        report = FinancialReport("FR001", "Q1 2024")

        result = report.generate(1000000, 1000000)

        self.assertEqual(result["profit"], 0)
        self.assertEqual(result["margin"], 0)

    def testFinancialReportStructure(self):
        """Тест структуры отчета"""
        report = FinancialReport("FR001", "Q1 2024")
        result = report.generate(1000000, 600000)

        # Проверяем наличие всех полей
        required_fields = ["report_id", "period", "revenue", "expenses", "profit", "margin"]
        for field in required_fields:
            self.assertIn(field, result)


if __name__ == '__main__':
    unittest.main()