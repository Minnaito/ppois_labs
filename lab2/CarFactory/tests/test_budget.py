import unittest
from config import constants
from models.finance.Budget import Budget


class TestBudget(unittest.TestCase):

    def testBudgetInitialization(self):
        """Тест инициализации бюджета"""
        budget = Budget("BUD001", 1000000)
        self.assertEqual(budget._budget_id, "BUD001")
        self.assertEqual(budget._total, 1000000)
        self.assertEqual(budget._spent, 0)

    def testSuccessfulSpend(self):
        """Тест успешной траты из бюджета"""
        budget = Budget("BUD001", 1000000)

        # Тратим часть бюджета
        result = budget.spend(300000)
        self.assertTrue(result)
        self.assertEqual(budget._spent, 300000)

        # Тратим еще
        result = budget.spend(200000)
        self.assertTrue(result)
        self.assertEqual(budget._spent, 500000)

    def testFailedSpendExceedsBudget(self):
        """Тест неудачной траты при превышении бюджета"""
        budget = Budget("BUD001", 1000000)

        # Тратим слишком много
        result = budget.spend(1200000)
        self.assertFalse(result)
        self.assertEqual(budget._spent, 0)

    def testFailedSpendExceedsRemaining(self):
        """Тест неудачной траты при превышении остатка"""
        budget = Budget("BUD001", 1000000)

        # Тратим часть
        budget.spend(800000)

        # Пытаемся потратить больше, чем осталось
        result = budget.spend(300000)
        self.assertFalse(result)
        self.assertEqual(budget._spent, 800000)

    def testCalculateRemaining(self):
        """Тест расчета остатка бюджета"""
        budget = Budget("BUD001", 1000000)

        # До трат
        remaining = budget.calculate_remaining()
        self.assertEqual(remaining, 1000000)

        # После трат
        budget.spend(400000)
        remaining = budget.calculate_remaining()
        self.assertEqual(remaining, 600000)

        # После всех трат
        budget.spend(600000)
        remaining = budget.calculate_remaining()
        self.assertEqual(remaining, 0)

    def testCalculateUtilization(self):
        """Тест расчета утилизации бюджета"""
        budget = Budget("BUD001", 1000000)

        # 0% утилизации
        utilization = budget.calculate_utilization()
        self.assertEqual(utilization, 0)

        # 30% утилизации
        budget.spend(300000)
        utilization = budget.calculate_utilization()
        self.assertEqual(utilization, 30)

        # 100% утилизации
        budget.spend(700000)
        utilization = budget.calculate_utilization()
        self.assertEqual(utilization, 100)

    def testCalculateUtilizationZeroBudget(self):
        """Тест расчета утилизации при нулевом бюджете"""
        budget = Budget("BUD001", 0)
        utilization = budget.calculate_utilization()
        self.assertEqual(utilization, 0)

    def testMultipleSpendOperations(self):
        """Тест множественных операций траты"""
        budget = Budget("BUD001", 5000000)

        operations = [
            (1000000, True),
            (1500000, True),
            (2000000, True),
            (600000, False),  # Превысит бюджет
            (500000, True)  # Последняя успешная
        ]

        for amount, expected_success in operations:
            result = budget.spend(amount)
            self.assertEqual(result, expected_success)

        # Проверяем итоговую сумму потраченных средств
        total_spent = 1000000 + 1500000 + 2000000 + 500000
        self.assertEqual(budget._spent, total_spent)

        # Проверяем остаток
        remaining = budget.calculate_remaining()
        self.assertEqual(remaining, 5000000 - total_spent)


if __name__ == '__main__':
    unittest.main()