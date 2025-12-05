import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.utilities.CalculationUtils import CalculationUtils

class TestCalculationUtilsExtended(unittest.TestCase):
    """Расширенные тесты для утилит расчетов"""

    def testCalculateTax(self):
        tax = CalculationUtils.calculateTax(1000)
        self.assertEqual(tax, 200.0)  # 20% от 1000

    def testCalculateDiscount(self):
        discount = CalculationUtils.calculateDiscount(1000, 0.1)
        self.assertEqual(discount, 100.0)

    def testCalculateAverage(self):
        average = CalculationUtils.calculateAverage([1, 2, 3, 4, 5])
        self.assertEqual(average, 3.0)

    def testCalculateEfficiency(self):
        efficiency = CalculationUtils.calculateEfficiency(85, 100)
        self.assertEqual(efficiency, 85.0)

    def testCalculateEfficiencyZeroTarget(self):
        efficiency = CalculationUtils.calculateEfficiency(85, 0)
        self.assertEqual(efficiency, 0.0)

if __name__ == '__main__':
    unittest.main()