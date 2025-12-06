import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from exceptions.ProductionExceptions.ProductionCapacityExceededError import ProductionCapacityExceededError


class TestProductionCapacityExceededError(unittest.TestCase):
    """Тесты для исключения превышения мощности"""

    def testProductionCapacityExceeded(self):
        with self.assertRaises(ProductionCapacityExceededError) as context:
            raise ProductionCapacityExceededError(1500, 1000)

        self.assertIn("Превышена производственная мощность", str(context.exception))


if __name__ == '__main__':
    unittest.main()