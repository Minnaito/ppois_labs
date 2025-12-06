import unittest
from config import constants
from models.utilities.CalculationUtils import CalculationUtils


class TestCalculationUtils(unittest.TestCase):

    def testCalculatePercentage(self):
        """Тест расчета процента"""
        # Нормальный случай
        percentage = CalculationUtils.calculatePercentage(25, 100)
        self.assertEqual(percentage, 25)

        # Часть больше целого
        percentage = CalculationUtils.calculatePercentage(150, 100)
        self.assertEqual(percentage, 150)

        # Ноль целого
        percentage = CalculationUtils.calculatePercentage(25, 0)
        self.assertEqual(percentage, 0)

        # Отрицательные значения
        percentage = CalculationUtils.calculatePercentage(-25, 100)
        self.assertEqual(percentage, -25)

    def testCalculateTax(self):
        """Тест расчета налога"""
        tax = CalculationUtils.calculateTax(100000)
        expected_tax = 100000 * constants.STANDARD_TAX_RATE
        self.assertEqual(tax, expected_tax)

        # С нулевой суммой
        tax = CalculationUtils.calculateTax(0)
        self.assertEqual(tax, 0)

        # С отрицательной суммой
        tax = CalculationUtils.calculateTax(-50000)
        self.assertEqual(tax, -50000 * constants.STANDARD_TAX_RATE)

    def testCalculateAverage(self):
        """Тест расчета среднего"""
        # Нормальный случай
        numbers = [10, 20, 30, 40, 50]
        average = CalculationUtils.calculateAverage(numbers)
        self.assertEqual(average, 30)

        # Один элемент
        numbers = [42]
        average = CalculationUtils.calculateAverage(numbers)
        self.assertEqual(average, 42)

        # С дробными числами
        numbers = [1.5, 2.5, 3.5]
        average = CalculationUtils.calculateAverage(numbers)
        self.assertAlmostEqual(average, 2.5)

        # Пустой список
        numbers = []
        average = CalculationUtils.calculateAverage(numbers)
        self.assertEqual(average, 0)

    def testCalculateEfficiency(self):
        """Тест расчета эффективности"""
        # 100% эффективность
        efficiency = CalculationUtils.calculateEfficiency(100, 100)
        self.assertEqual(efficiency, 100)

        # 50% эффективность
        efficiency = CalculationUtils.calculateEfficiency(50, 100)
        self.assertEqual(efficiency, 50)

        # 150% эффективность (ограничивается 100%)
        efficiency = CalculationUtils.calculateEfficiency(150, 100)
        self.assertEqual(efficiency, 100)

        # Ноль цели
        efficiency = CalculationUtils.calculateEfficiency(50, 0)
        self.assertEqual(efficiency, 0)

        # Отрицательные значения
        efficiency = CalculationUtils.calculateEfficiency(-50, 100)
        self.assertEqual(efficiency, -50)

    def testCalculateMaterialCost(self):
        """Тест расчета стоимости материала"""
        cost = CalculationUtils.calculateMaterialCost(100)
        expected_cost = 100 * constants.MATERIAL_COST_MULTIPLIER
        self.assertEqual(cost, expected_cost)

        # Нулевое количество
        cost = CalculationUtils.calculateMaterialCost(0)
        self.assertEqual(cost, 0)

        # Отрицательное количество
        cost = CalculationUtils.calculateMaterialCost(-50)
        self.assertEqual(cost, -50 * constants.MATERIAL_COST_MULTIPLIER)

    def testAllCalculationsTogether(self):
        """Тест всех расчетов вместе"""
        # Тестовые данные
        material_quantity = 500
        tax_amount = 100000
        actual_production = 850
        target_production = 1000
        part_value = 75
        whole_value = 150

        # Выполняем все расчеты
        material_cost = CalculationUtils.calculateMaterialCost(material_quantity)
        tax = CalculationUtils.calculateTax(tax_amount)
        efficiency = CalculationUtils.calculateEfficiency(actual_production, target_production)
        percentage = CalculationUtils.calculatePercentage(part_value, whole_value)
        average = CalculationUtils.calculateAverage([10, 20, 30])

        # Проверяем результаты
        self.assertEqual(material_cost, material_quantity * constants.MATERIAL_COST_MULTIPLIER)
        self.assertEqual(tax, tax_amount * constants.STANDARD_TAX_RATE)
        self.assertEqual(efficiency, 85)  # 850/1000*100 = 85%
        self.assertEqual(percentage, 50)  # 75/150*100 = 50%
        self.assertEqual(average, 20)


if __name__ == '__main__':
    unittest.main()