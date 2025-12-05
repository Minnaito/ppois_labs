import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from exceptions.FinanceExceptions.InsufficientFundsError import InsufficientFundsError


class TestInsufficientFundsError(unittest.TestCase):
    """Тесты для исключения недостатка средств"""

    def testInsufficientFunds(self):
        with self.assertRaises(InsufficientFundsError) as context:
            raise InsufficientFundsError(500.0, 1000.0)

        self.assertIn("Недостаточно средств", str(context.exception))


if __name__ == '__main__':
    unittest.main()