import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.finance.Budget import Budget
from exceptions.FinanceExceptions.BudgetExceededError import BudgetExceededError


class TestBudget(unittest.TestCase):
    """Тесты для бюджета"""

    def setUp(self):
        self.budget = Budget("BUDGET001", "Производственный бюджет", 100000.0, "2024")

    def testBudgetInitialization(self):
        """Тест инициализации бюджета"""
        self.assertEqual(self.budget._budgetId, "BUDGET001")
        self.assertEqual(self.budget._budgetName, "Производственный бюджет")
        self.assertEqual(self.budget._totalAmount, 100000.0)
        self.assertEqual(self.budget._budgetPeriod, "2024")
        self.assertEqual(self.budget._allocatedAmount, 0.0)
        self.assertEqual(self.budget._spentAmount, 0.0)
        self.assertEqual(self.budget._remainingAmount, 100000.0)
        self.assertEqual(self.budget._budgetCategories, {})
        self.assertTrue(self.budget._isActive)

    def testBudgetAllocation(self):
        """Тест распределения средств"""
        success = self.budget.allocateFunds("Материалы", 50000.0)
        self.assertTrue(success)
        self.assertEqual(self.budget._allocatedAmount, 50000.0)
        self.assertEqual(self.budget._remainingAmount, 50000.0)
        self.assertEqual(self.budget._budgetCategories["Материалы"], 50000.0)

    def testBudgetAllocationExceeded(self):
        """Тест превышения бюджета при распределении"""
        success = self.budget.allocateFunds("Материалы", 150000.0)
        self.assertFalse(success)
        self.assertEqual(self.budget._allocatedAmount, 0.0)
        self.assertEqual(self.budget._remainingAmount, 100000.0)

    def testMultipleAllocations(self):
        """Тест нескольких распределений средств"""
        self.budget.allocateFunds("Материалы", 30000.0)
        self.budget.allocateFunds("Зарплаты", 40000.0)
        self.assertEqual(self.budget._allocatedAmount, 70000.0)
        self.assertEqual(self.budget._remainingAmount, 30000.0)
        self.assertEqual(len(self.budget._budgetCategories), 2)

    def testRecordExpense(self):
        """Тест записи расходов"""
        self.budget.allocateFunds("Материалы", 50000.0)
        self.budget.recordExpense("Материалы", 20000.0)
        self.assertEqual(self.budget._spentAmount, 20000.0)
        self.assertEqual(self.budget._remainingAmount, 30000.0)

    def testRecordExpenseExceeded(self):
        """Тест превышения бюджета при расходовании"""
        self.budget.allocateFunds("Материалы", 50000.0)
        with self.assertRaises(BudgetExceededError):
            self.budget.recordExpense("Материалы", 60000.0)

    def testRecordExpenseUnknownCategory(self):
        """Тест расхода по неизвестной категории"""
        with self.assertRaises(ValueError):  # <--- Добавьте этот контекстный менеджер
            self.budget.recordExpense("Неизвестная категория", 10000.0)

    def testCalculateUtilizationPercentage(self):
        """Тест расчета процента использования бюджета"""
        self.budget.allocateFunds("Материалы", 50000.0)
        self.budget.recordExpense("Материалы", 25000.0)
        utilization = self.budget.calculateUtilizationPercentage()
        expected_utilization = (25000.0 / 100000.0) * 100
        self.assertEqual(utilization, expected_utilization)

    def testCalculateUtilizationPercentageZeroBudget(self):
        """Тест расчета процента использования при нулевом бюджете"""
        zero_budget = Budget("BUDGET002", "Нулевой бюджет", 0.0, "2024")
        utilization = zero_budget.calculateUtilizationPercentage()
        self.assertEqual(utilization, 0.0)

    def testGetBudgetStatus(self):
        """Тест получения статуса бюджета"""
        self.budget.allocateFunds("Материалы", 50000.0)
        self.budget.recordExpense("Материалы", 20000.0)

        status = self.budget.getBudgetStatus()

        self.assertEqual(status["budgetId"], "BUDGET001")
        self.assertEqual(status["budgetName"], "Производственный бюджет")
        self.assertEqual(status["totalAmount"], 100000.0)
        self.assertEqual(status["allocatedAmount"], 50000.0)
        self.assertEqual(status["spentAmount"], 20000.0)
        self.assertEqual(status["remainingAmount"], 30000.0)
        self.assertEqual(status["categoriesCount"], 1)
        self.assertTrue(status["isActive"])
        self.assertGreater(status["utilizationPercentage"], 0)

    def testZeroAllocation(self):
        """Тест распределения нулевой суммы"""
        success = self.budget.allocateFunds("Маркетинг", 0.0)
        self.assertTrue(success)
        self.assertEqual(self.budget._allocatedAmount, 0.0)
        self.assertEqual(self.budget._remainingAmount, 100000.0)

    def testMultipleExpensesSameCategory(self):
        """Тест нескольких расходов по одной категории"""
        self.budget.allocateFunds("Материалы", 50000.0)
        self.budget.recordExpense("Материалы", 10000.0)
        self.budget.recordExpense("Материалы", 15000.0)
        self.assertEqual(self.budget._spentAmount, 25000.0)
        self.assertEqual(self.budget._remainingAmount, 25000.0)

    def testBudgetWithDifferentPeriods(self):
        """Тест бюджетов с разными периодами"""
        monthly_budget = Budget("MONTH001", "Месячный бюджет", 50000.0, "2024-01")
        quarterly_budget = Budget("QTR001", "Квартальный бюджет", 150000.0, "2024-Q1")

        self.assertEqual(monthly_budget._budgetPeriod, "2024-01")
        self.assertEqual(quarterly_budget._budgetPeriod, "2024-Q1")


if __name__ == '__main__':
    unittest.main()