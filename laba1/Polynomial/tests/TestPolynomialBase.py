import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.PolynomialBase import PolynomialBase


class TestPolynomialBase(unittest.TestCase):

    def testInitialization(self):
        """Тесты инициализации многочлена."""
        polynomialFirst = PolynomialBase([2, -3, 1])
        self.assertEqual(polynomialFirst.coefficients, [2, -3, 1])
        self.assertEqual(polynomialFirst.degree, 2)

    def testGetItem(self):
        """Тесты оператора []."""
        testPolynomial = PolynomialBase([2, -3, 1])
        self.assertEqual(testPolynomial[0], 2)
        self.assertEqual(testPolynomial[1], -3)
        self.assertEqual(testPolynomial[2], 1)

    def testCallOperator(self):
        """Тесты вычисления значения."""
        testPolynomial = PolynomialBase([2, -3, 1])
        self.assertEqual(testPolynomial(0), 1)
        self.assertEqual(testPolynomial(1), 0)
        self.assertEqual(testPolynomial(2), 3)

    def testStringRepresentation(self):
        """Тесты строкового представления."""
        self.assertEqual(str(PolynomialBase([2, -3, 1])), "2x^2 -3x +1")
        self.assertEqual(str(PolynomialBase([5])), "5")

    def testCopy(self):
        """Тест копирования."""
        polynomialOriginal = PolynomialBase([2, -3, 1])
        polynomialCopy = polynomialOriginal.copy()

        self.assertEqual(polynomialOriginal.coefficients, polynomialCopy.coefficients)
        self.assertIsNot(polynomialOriginal, polynomialCopy)


if __name__ == '__main__':
    unittest.main()
