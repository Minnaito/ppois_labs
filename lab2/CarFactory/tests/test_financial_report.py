import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.finance.FinancialReport import FinancialReport
from config import constants


class TestFinancialReport(unittest.TestCase):
    """Тесты для класса FinancialReport"""

    def setUp(self):
        self.financial_report = FinancialReport("REP001", "Q1 2024")

    def test_financial_report_initialization(self):
        self.assertEqual(self.financial_report._reportId, "REP001")
        self.assertEqual(self.financial_report._reportPeriod, "Q1 2024")
        self.assertEqual(self.financial_report._revenue, 0.0)
        self.assertEqual(self.financial_report._expenses, 0.0)
        self.assertEqual(self.financial_report._profit, 0.0)
        self.assertEqual(self.financial_report._assets, 0.0)
        self.assertEqual(self.financial_report._liabilities, 0.0)
        self.assertEqual(self.financial_report._equity, 0.0)
        self.assertIsNotNone(self.financial_report._reportDate)

    def test_add_revenue(self):
        self.financial_report.addRevenue(1000.0)
        self.assertEqual(self.financial_report._revenue, 1000.0)
        self.assertEqual(self.financial_report._profit, 1000.0)  # revenue - expenses (0)

    def test_add_multiple_revenues(self):
        revenues = [500.0, 750.0, 300.0]
        for revenue in revenues:
            self.financial_report.addRevenue(revenue)

        self.assertEqual(self.financial_report._revenue, 1550.0)
        self.assertEqual(self.financial_report._profit, 1550.0)

    def test_add_expense(self):
        self.financial_report.addRevenue(2000.0)
        self.financial_report.addExpense(800.0)
        self.assertEqual(self.financial_report._expenses, 800.0)
        self.assertEqual(self.financial_report._profit, 1200.0)  # 2000 - 800

    def test_add_multiple_expenses(self):
        self.financial_report.addRevenue(3000.0)
        expenses = [500.0, 300.0, 200.0]
        for expense in expenses:
            self.financial_report.addExpense(expense)

        self.assertEqual(self.financial_report._expenses, 1000.0)
        self.assertEqual(self.financial_report._profit, 2000.0)  # 3000 - 1000

    def test_calculate_profit_margin_positive(self):
        self.financial_report.addRevenue(2000.0)
        self.financial_report.addExpense(1200.0)

        margin = self.financial_report.calculateProfitMargin()
        expected_margin = (800.0 / 2000.0) * constants.PERCENTAGE_MULTIPLIER  # (800/2000)*100 = 40%
        self.assertEqual(margin, expected_margin)

    def test_calculate_profit_margin_zero_revenue(self):
        margin = self.financial_report.calculateProfitMargin()
        self.assertEqual(margin, constants.ZERO_VALUE)

    def test_calculate_profit_margin_negative_profit(self):
        self.financial_report.addRevenue(1000.0)
        self.financial_report.addExpense(1500.0)  # Убыток

        margin = self.financial_report.calculateProfitMargin()
        expected_margin = (-500.0 / 1000.0) * constants.PERCENTAGE_MULTIPLIER  # -50%
        self.assertEqual(margin, expected_margin)

    def test_calculate_debt_to_equity_ratio_positive(self):
        self.financial_report._liabilities = 600.0
        self.financial_report._equity = 400.0

        ratio = self.financial_report.calculateDebtToEquityRatio()
        expected_ratio = 600.0 / 400.0  # 1.5
        self.assertEqual(ratio, expected_ratio)

    def test_calculate_debt_to_equity_ratio_zero_equity(self):
        self.financial_report._liabilities = 500.0
        self.financial_report._equity = 0.0

        ratio = self.financial_report.calculateDebtToEquityRatio()
        self.assertEqual(ratio, 0.0)

    def test_calculate_debt_to_equity_ratio_zero_liabilities(self):
        self.financial_report._liabilities = 0.0
        self.financial_report._equity = 1000.0

        ratio = self.financial_report.calculateDebtToEquityRatio()
        self.assertEqual(ratio, 0.0)

    def test_generate_report_basic(self):
        report = self.financial_report.generateReport()

        self.assertEqual(report["reportId"], "REP001")
        self.assertEqual(report["reportPeriod"], "Q1 2024")
        self.assertEqual(report["revenue"], 0.0)
        self.assertEqual(report["expenses"], 0.0)
        self.assertEqual(report["profit"], 0.0)
        self.assertEqual(report["assets"], 0.0)
        self.assertEqual(report["liabilities"], 0.0)
        self.assertEqual(report["equity"], 0.0)
        self.assertEqual(report["profitMarginPercentage"], constants.ZERO_VALUE)
        self.assertEqual(report["debtToEquityRatio"], 0.0)
        self.assertIsNotNone(report["reportDate"])

    def test_generate_report_with_data(self):
        # Устанавливаем финансовые данные
        self.financial_report.addRevenue(5000.0)
        self.financial_report.addExpense(3000.0)
        self.financial_report._assets = 10000.0
        self.financial_report._liabilities = 4000.0
        self.financial_report._equity = 6000.0

        report = self.financial_report.generateReport()

        self.assertEqual(report["revenue"], 5000.0)
        self.assertEqual(report["expenses"], 3000.0)
        self.assertEqual(report["profit"], 2000.0)
        self.assertEqual(report["assets"], 10000.0)
        self.assertEqual(report["liabilities"], 4000.0)
        self.assertEqual(report["equity"], 6000.0)

        # Проверяем расчетные поля
        expected_margin = (2000.0 / 5000.0) * constants.PERCENTAGE_MULTIPLIER  # 40%
        expected_ratio = 4000.0 / 6000.0  # ~0.666

        self.assertEqual(report["profitMarginPercentage"], expected_margin)
        self.assertEqual(report["debtToEquityRatio"], expected_ratio)

    def test_profit_calculation_automatically(self):
        # Проверяем, что прибыль пересчитывается автоматически
        self.financial_report.addRevenue(1000.0)
        self.assertEqual(self.financial_report._profit, 1000.0)

        self.financial_report.addExpense(400.0)
        self.assertEqual(self.financial_report._profit, 600.0)

        self.financial_report.addRevenue(500.0)
        self.assertEqual(self.financial_report._profit, 1100.0)

        self.financial_report.addExpense(200.0)
        self.assertEqual(self.financial_report._profit, 900.0)

    def test_report_date_format(self):
        report = self.financial_report.generateReport()
        date_parts = report["reportDate"].split("-")

        self.assertEqual(len(date_parts), 3)
        self.assertEqual(len(date_parts[0]), 4)  # Год
        self.assertEqual(len(date_parts[1]), 2)  # Месяц
        self.assertEqual(len(date_parts[2]), 2)  # День

    def test_complete_financial_scenario(self):
        # Полный финансовый сценарий
        self.financial_report.addRevenue(10000.0)  # Доходы
        self.financial_report.addExpense(6000.0)  # Расходы
        self.financial_report._assets = 20000.0  # Активы
        self.financial_report._liabilities = 8000.0  # Обязательства
        self.financial_report._equity = 12000.0  # Капитал

        report = self.financial_report.generateReport()

        # Проверяем основные показатели
        self.assertEqual(report["revenue"], 10000.0)
        self.assertEqual(report["expenses"], 6000.0)
        self.assertEqual(report["profit"], 4000.0)
        self.assertEqual(report["assets"], 20000.0)
        self.assertEqual(report["liabilities"], 8000.0)
        self.assertEqual(report["equity"], 12000.0)

        # Проверяем финансовые коэффициенты
        expected_margin = (4000.0 / 10000.0) * constants.PERCENTAGE_MULTIPLIER  # 40%
        expected_ratio = 8000.0 / 12000.0  # ~0.666

        self.assertEqual(report["profitMarginPercentage"], expected_margin)
        self.assertEqual(report["debtToEquityRatio"], expected_ratio)


if __name__ == '__main__':
    unittest.main()