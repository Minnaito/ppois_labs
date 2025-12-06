import unittest
import sys
import os

# Добавляем путь для импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import constants
from models.utilities.CalculationUtils import CalculationUtils


class TestCalculationUtilsExtended(unittest.TestCase):
    """Расширенные тесты для утилит расчета"""

    def testCalculatePercentageEdgeCases(self):
        """Тест расчета процента для крайних случаев"""
        # Очень большие числа
        percentage = CalculationUtils.calculatePercentage(10 ** 9, 10 ** 9)
        self.assertEqual(percentage, 100)

        # Очень маленькие числа
        percentage = CalculationUtils.calculatePercentage(0.0001, 0.0001)
        self.assertEqual(percentage, 100)

        # Деление на очень маленькое число (не ноль)
        percentage = CalculationUtils.calculatePercentage(1, 0.000001)
        self.assertEqual(percentage, 100000000)  # 1 / 0.000001 * 100

    def testCalculateTaxSpecialCases(self):
        """Тест расчета налога для специальных случаев"""
        # Ноль
        tax = CalculationUtils.calculateTax(0)
        self.assertEqual(tax, 0)

        # Отрицательное значение
        tax = CalculationUtils.calculateTax(-1000)
        expected_tax = -1000 * constants.STANDARD_TAX_RATE
        self.assertEqual(tax, expected_tax)

        # Очень большая сумма
        large_amount = 10 ** 12  # 1 триллион
        tax = CalculationUtils.calculateTax(large_amount)
        expected_tax = large_amount * constants.STANDARD_TAX_RATE
        self.assertEqual(tax, expected_tax)

    def testCalculateAverageComplexScenarios(self):
        """Тест расчета среднего для сложных сценариев"""
        # Большой список
        large_list = list(range(1, 1001))  # числа от 1 до 1000
        average = CalculationUtils.calculateAverage(large_list)
        expected_average = sum(large_list) / len(large_list)
        self.assertEqual(average, expected_average)

        # Список с None (должен вызвать ошибку при использовании)
        # Ожидаем TypeError при попытке сложения
        with self.assertRaises(TypeError):
            CalculationUtils.calculateAverage([1, 2, None, 4])

        # Смешанные типы (int и float)
        mixed_list = [1, 2.5, 3, 4.75, 5]
        average = CalculationUtils.calculateAverage(mixed_list)
        expected_average = sum(mixed_list) / len(mixed_list)
        self.assertEqual(average, expected_average)

    def testCalculateEfficiencySpecialCases(self):
        """Тест расчета эффективности для специальных случаев"""
        # Эффективность 0%
        efficiency = CalculationUtils.calculateEfficiency(0, 100)
        self.assertEqual(efficiency, 0)

        # Эффективность > 100% (ограничивается 100%)
        efficiency = CalculationUtils.calculateEfficiency(200, 150)
        self.assertEqual(efficiency, 100)

        # Отрицательная эффективность
        efficiency = CalculationUtils.calculateEfficiency(-50, 100)
        self.assertEqual(efficiency, -50)

        # Отрицательная цель
        efficiency = CalculationUtils.calculateEfficiency(50, -100)
        self.assertEqual(efficiency, -50)

    def testCalculateMaterialCostSpecialCases(self):
        """Тест расчета стоимости материала для специальных случаев"""
        # Дробное количество
        cost = CalculationUtils.calculateMaterialCost(12.5)
        expected_cost = 12.5 * constants.MATERIAL_COST_MULTIPLIER
        self.assertEqual(cost, expected_cost)

        # Очень большое количество
        large_quantity = 10 ** 6  # 1 миллион
        cost = CalculationUtils.calculateMaterialCost(large_quantity)
        expected_cost = large_quantity * constants.MATERIAL_COST_MULTIPLIER
        self.assertEqual(cost, expected_cost)

        # Отрицательное количество
        cost = CalculationUtils.calculateMaterialCost(-100)
        expected_cost = -100 * constants.MATERIAL_COST_MULTIPLIER
        self.assertEqual(cost, expected_cost)

    def testIntegrationWithConstants(self):
        """Тест интеграции с константами"""
        # Проверяем, что используются правильные константы
        test_amount = 1000

        # Проверяем налог
        tax = CalculationUtils.calculateTax(test_amount)
        self.assertEqual(tax, test_amount * constants.STANDARD_TAX_RATE)

        # Проверяем стоимость материала
        material_cost = CalculationUtils.calculateMaterialCost(test_amount)
        self.assertEqual(material_cost, test_amount * constants.MATERIAL_COST_MULTIPLIER)

        # Проверяем, что процентный множитель корректен
        efficiency = CalculationUtils.calculateEfficiency(75, 100)
        self.assertEqual(efficiency, 75)  # 75/100 * 100 = 75

    def testErrorHandling(self):
        """Тест обработки ошибок"""
        # Пустой список для среднего
        average = CalculationUtils.calculateAverage([])
        self.assertEqual(average, 0)

        # Деление на ноль в процентах
        percentage = CalculationUtils.calculatePercentage(100, 0)
        self.assertEqual(percentage, 0)

        # Деление на ноль в эффективности
        efficiency = CalculationUtils.calculateEfficiency(100, 0)
        self.assertEqual(efficiency, 0)

    def testPerformance(self):
        """Тест производительности (должен выполняться быстро)"""
        import time

        start_time = time.time()

        # Множественные вычисления
        for i in range(10000):
            CalculationUtils.calculatePercentage(i, i + 1)
            CalculationUtils.calculateTax(i * 1000)
            CalculationUtils.calculateAverage([i, i + 1, i + 2])
            CalculationUtils.calculateEfficiency(i, i + 100)
            CalculationUtils.calculateMaterialCost(i)

        end_time = time.time()
        execution_time = end_time - start_time

        # Должно выполняться менее 1 секунды
        self.assertLess(execution_time, 1.0)
        print(f"Тест производительности: {execution_time:.3f} секунд")


if __name__ == '__main__':
    unittest.main()