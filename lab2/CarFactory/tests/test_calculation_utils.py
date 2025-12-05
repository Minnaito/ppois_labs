import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.utilities.CalculationUtils import CalculationUtils


class TestCalculationUtils(unittest.TestCase):
    """Тесты для утилит расчетов"""

    def testCalculatePercentage(self):
        percentage = CalculationUtils.calculatePercentage(25, 100)
        self.assertEqual(percentage, 25.0)

    def testCalculateAverage(self):
        average = CalculationUtils.calculateAverage([1, 2, 3, 4, 5])
        self.assertEqual(average, 3.0)


if __name__ == '__main__':
    unittest.main()