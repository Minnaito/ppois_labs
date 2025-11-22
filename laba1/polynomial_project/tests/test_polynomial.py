import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.polynomial import polynomial


class test_polynomial(unittest.TestCase):

    def test_addition(self):
        """Тест сложения многочленов."""
        polynomial_first = polynomial([2, -3, 1])
        polynomial_second = polynomial([1, 2])
        result_polynomial = polynomial_first + polynomial_second
        self.assertEqual(result_polynomial.coefficients, [2, -2, 3])

    def test_subtraction(self):
        """Тест вычитания многочленов."""
        polynomial_first = polynomial([2, -3, 1])
        polynomial_second = polynomial([1, 2])
        result_polynomial = polynomial_first - polynomial_second
        self.assertEqual(result_polynomial.coefficients, [2, -4, -1])

    def test_multiplication(self):
        """Тест умножения многочленов."""
        polynomial_first = polynomial([2, 1])
        polynomial_second = polynomial([3, 2])
        result_polynomial = polynomial_first * polynomial_second
        self.assertEqual(result_polynomial.coefficients, [6, 7, 2])

    def test_division(self):
        """Тест деления многочленов."""
        polynomial_first = polynomial([2, -3, 1])
        polynomial_second = polynomial([1, -1])
        result_polynomial = polynomial_first / polynomial_second
        self.assertEqual(result_polynomial.coefficients, [2, -1])

    def test_inplace_addition(self):
        """Тест сложения с присваиванием."""
        polynomial_first = polynomial([2, -3, 1])
        polynomial_second = polynomial([1, 2])
        original_id_value = id(polynomial_first)

        polynomial_first += polynomial_second
        self.assertEqual(polynomial_first.coefficients, [2, -2, 3])
        self.assertEqual(id(polynomial_first), original_id_value)

    def test_inplace_subtraction(self):
        """Тест вычитания с присваиванием."""
        polynomial_first = polynomial([2, -3, 1])
        polynomial_second = polynomial([1, 2])
        original_id_value = id(polynomial_first)

        polynomial_first -= polynomial_second
        self.assertEqual(polynomial_first.coefficients, [2, -4, -1])
        self.assertEqual(id(polynomial_first), original_id_value)

    def test_inplace_multiplication(self):
        """Тест умножения с присваиванием."""
        polynomial_first = polynomial([2, 1])
        polynomial_second = polynomial([3, 2])
        original_id_value = id(polynomial_first)

        polynomial_first *= polynomial_second
        self.assertEqual(polynomial_first.coefficients, [6, 7, 2])
        self.assertEqual(id(polynomial_first), original_id_value)

    def test_division_by_zero(self):
        """Тест деления на ноль."""
        test_polynomial = polynomial([1, 2, 3])
        with self.assertRaises(ZeroDivisionError):
            test_polynomial / 0

    def test_addition_with_scalar(self):
        """Тест сложения со скаляром."""
        polynomial_first = polynomial([2, -3, 1])
        result_polynomial = polynomial_first + 5
        self.assertEqual(result_polynomial.coefficients, [2, -3, 6])

    def test_multiplication_with_scalar(self):
        """Тест умножения на скаляр."""
        polynomial_first = polynomial([2, -3, 1])
        result_polynomial = polynomial_first * 3
        self.assertEqual(result_polynomial.coefficients, [6, -9, 3])


if __name__ == '__main__':
    unittest.main()
