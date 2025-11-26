import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.Polynomial import Polynomial


class TestPolynomial(unittest.TestCase):

    def testAddition(self):
        """Тест сложения многочленов."""
        polynomialFirst = Polynomial([2, -3, 1])
        polynomialSecond = Polynomial([1, 2])
        resultPolynomial = polynomialFirst + polynomialSecond
        self.assertEqual(resultPolynomial.coefficients, [2, -2, 3])

    def testSubtraction(self):
        """Тест вычитания многочленов."""
        polynomialFirst = Polynomial([2, -3, 1])
        polynomialSecond = Polynomial([1, 2])
        resultPolynomial = polynomialFirst - polynomialSecond
        self.assertEqual(resultPolynomial.coefficients, [2, -4, -1])

    def testMultiplication(self):
        """Тест умножения многочленов."""
        polynomialFirst = Polynomial([2, 1])
        polynomialSecond = Polynomial([3, 2])
        resultPolynomial = polynomialFirst * polynomialSecond
        self.assertEqual(resultPolynomial.coefficients, [6, 7, 2])

    def testDivision(self):
        """Тест деления многочленов."""
        polynomialFirst = Polynomial([2, -3, 1])
        polynomialSecond = Polynomial([1, -1])
        resultPolynomial = polynomialFirst / polynomialSecond
        self.assertEqual(resultPolynomial.coefficients, [2, -1])

    def testInplaceAddition(self):
        """Тест сложения с присваиванием."""
        polynomialFirst = Polynomial([2, -3, 1])
        polynomialSecond = Polynomial([1, 2])
        originalIdValue = id(polynomialFirst)

        polynomialFirst += polynomialSecond
        self.assertEqual(polynomialFirst.coefficients, [2, -2, 3])
        self.assertEqual(id(polynomialFirst), originalIdValue)

    def testInplaceSubtraction(self):
        """Тест вычитания с присваиванием."""
        polynomialFirst = Polynomial([2, -3, 1])
        polynomialSecond = Polynomial([1, 2])
        originalIdValue = id(polynomialFirst)

        polynomialFirst -= polynomialSecond
        self.assertEqual(polynomialFirst.coefficients, [2, -4, -1])
        self.assertEqual(id(polynomialFirst), originalIdValue)

    def testInplaceMultiplication(self):
        """Тест умножения с присваиванием."""
        polynomialFirst = Polynomial([2, 1])
        polynomialSecond = Polynomial([3, 2])
        originalIdValue = id(polynomialFirst)

        polynomialFirst *= polynomialSecond
        self.assertEqual(polynomialFirst.coefficients, [6, 7, 2])
        self.assertEqual(id(polynomialFirst), originalIdValue)

    def testDivisionByZero(self):
        """Тест деления на ноль."""
        testPolynomial = Polynomial([1, 2, 3])
        with self.assertRaises(ZeroDivisionError):
            testPolynomial / 0

    def testAdditionWithScalar(self):
        """Тест сложения со скаляром."""
        polynomialFirst = Polynomial([2, -3, 1])
        resultPolynomial = polynomialFirst + 5
        self.assertEqual(resultPolynomial.coefficients, [2, -3, 6])

    def testMultiplicationWithScalar(self):
        """Тест умножения на скаляр."""
        polynomialFirst = Polynomial([2, -3, 1])
        resultPolynomial = polynomialFirst * 3
        self.assertEqual(resultPolynomial.coefficients, [6, -9, 3])


if __name__ == '__main__':
    unittest.main()
