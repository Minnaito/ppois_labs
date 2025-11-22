import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.polynomial_base import polynomial_base


class test_polynomial_base(unittest.TestCase):

    def test_initialization(self):
        """Тесты инициализации многочлена."""
        polynomial_first = polynomial_base([2, -3, 1])
        self.assertEqual(polynomial_first.coefficients, [2, -3, 1])
        self.assertEqual(polynomial_first.degree, 2)

    def test_getitem(self):
        """Тесты оператора []."""
        test_polynomial = polynomial_base([2, -3, 1])
        self.assertEqual(test_polynomial[0], 2)
        self.assertEqual(test_polynomial[1], -3)
        self.assertEqual(test_polynomial[2], 1)

    def test_call_operator(self):
        """Тесты вычисления значения."""
        test_polynomial = polynomial_base([2, -3, 1])
        self.assertEqual(test_polynomial(0), 1)
        self.assertEqual(test_polynomial(1), 0)
        self.assertEqual(test_polynomial(2), 3)

    def test_string_representation(self):
        """Тесты строкового представления."""
        self.assertEqual(str(polynomial_base([2, -3, 1])), "2x^2 -3x +1")
        self.assertEqual(str(polynomial_base([5])), "5")

    def test_copy(self):
        """Тест копирования."""
        polynomial_original = polynomial_base([2, -3, 1])
        polynomial_copy = polynomial_original.copy()

        self.assertEqual(polynomial_original.coefficients, polynomial_copy.coefficients)
        self.assertIsNot(polynomial_original, polynomial_copy)


if __name__ == '__main__':
    unittest.main()
