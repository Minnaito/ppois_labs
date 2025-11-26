import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.PolynomialBase import PolynomialBase
from src.Polynomial import Polynomial


class TestComprehensive(unittest.TestCase):

    def testPolynomialCreation(self):
        """Тест создания многочлена."""
        testPolynomial = Polynomial([1, 2, 3])
        self.assertEqual(testPolynomial.coefficients, [1, 2, 3])
        self.assertEqual(testPolynomial.degree, 2)

    def testZeroPolynomial(self):
        """Тест нулевого многочлена."""
        zeroPolynomial = Polynomial([0])
        self.assertEqual(zeroPolynomial.degree, 0)
        self.assertEqual(zeroPolynomial(5), 0)

    def testConstantPolynomial(self):
        """Тест константного многочлена."""
        constantPoly = Polynomial([7])
        self.assertEqual(constantPoly.degree, 0)
        self.assertEqual(constantPoly(10), 7)

    def testLeadingZerosRemoval(self):
        """Тест удаления ведущих нулей."""
        polynomialWithZeros = Polynomial([0, 0, 3, 2])
        self.assertEqual(polynomialWithZeros.coefficients, [3, 2])
        self.assertEqual(polynomialWithZeros.degree, 1)

    def testPolynomialStringFormat(self):
        """Тест форматирования строки."""
        polyOne = Polynomial([1, -2, 1])
        self.assertEqual(str(polyOne), "1x^2 -2x +1")

        polyTwo = Polynomial([-1, 0, 1])
        self.assertEqual(str(polyTwo), "-1x^2 +1")

    def testPolynomialEvaluation(self):
        """Тест вычисления значения."""
        testPoly = Polynomial([2, -1, 3])
        self.assertEqual(testPoly(0), 3)
        self.assertEqual(testPoly(1), 4)
        self.assertEqual(testPoly(2), 9)

    def testCoefficientAccess(self):
        """Тест доступа к коэффициентам."""
        testPoly = Polynomial([4, 3, 2, 1])
        self.assertEqual(testPoly[0], 4)
        self.assertEqual(testPoly[1], 3)
        self.assertEqual(testPoly[2], 2)
        self.assertEqual(testPoly[3], 1)

    def testAdditionCommutative(self):
        """Тест коммутативности сложения."""
        polyFirst = Polynomial([1, 2])
        polySecond = Polynomial([3, 4])
        resultOne = polyFirst + polySecond
        resultTwo = polySecond + polyFirst
        self.assertEqual(resultOne.coefficients, resultTwo.coefficients)

    def testMultiplicationCommutative(self):
        """Тест коммутативности умножения."""
        polyFirst = Polynomial([1, 2])
        polySecond = Polynomial([3, 4])
        resultOne = polyFirst * polySecond
        resultTwo = polySecond * polyFirst
        self.assertEqual(resultOne.coefficients, resultTwo.coefficients)

    def testAdditionAssociativity(self):
        """Тест ассоциативности сложения."""
        polyFirst = Polynomial([1, 2])
        polySecond = Polynomial([3, 4])
        polyThird = Polynomial([5, 6])

        leftResult = (polyFirst + polySecond) + polyThird
        rightResult = polyFirst + (polySecond + polyThird)
        self.assertEqual(leftResult.coefficients, rightResult.coefficients)

    def testMultiplicationAssociativity(self):
        """Тест ассоциативности умножения."""
        polyFirst = Polynomial([1, 1])
        polySecond = Polynomial([2, 1])
        polyThird = Polynomial([3, 1])

        leftResult = (polyFirst * polySecond) * polyThird
        rightResult = polyFirst * (polySecond * polyThird)
        self.assertEqual(leftResult.coefficients, rightResult.coefficients)

    def testDistributiveProperty(self):
        """Тест дистрибутивности."""
        polyFirst = Polynomial([1, 2])
        polySecond = Polynomial([3, 4])
        polyThird = Polynomial([5, 6])

        leftSide = polyFirst * (polySecond + polyThird)
        rightSide = (polyFirst * polySecond) + (polyFirst * polyThird)
        self.assertEqual(leftSide.coefficients, rightSide.coefficients)

    def testIdentityAddition(self):
        """Тест сложения с нулевым многочленом."""
        testPoly = Polynomial([1, 2, 3])
        zeroPoly = Polynomial([0])
        resultPoly = testPoly + zeroPoly
        self.assertEqual(resultPoly.coefficients, testPoly.coefficients)

    def testIdentityMultiplication(self):
        """Тест умножения на единичный многочлен."""
        testPoly = Polynomial([1, 2, 3])
        onePoly = Polynomial([1])
        resultPoly = testPoly * onePoly
        self.assertEqual(resultPoly.coefficients, testPoly.coefficients)

    def testZeroMultiplication(self):
        """Тест умножения на ноль."""
        testPoly = Polynomial([1, 2, 3])
        zeroPoly = Polynomial([0])
        resultPoly = testPoly * zeroPoly
        self.assertEqual(resultPoly.coefficients, [0])

    def testDivisionByHigherDegree(self):
        """Тест деления на многочлен большей степени."""
        polyNumerator = Polynomial([1, 2])
        polyDenominator = Polynomial([1, 0, 1])
        resultPoly = polyNumerator / polyDenominator
        self.assertEqual(resultPoly.coefficients, [0])

    def testExactDivision(self):
        """Тест точного деления."""
        polyNumerator = Polynomial([1, 3, 3, 1])
        polyDenominator = Polynomial([1, 1])
        resultPoly = polyNumerator / polyDenominator
        self.assertEqual(resultPoly.coefficients, [1, 2, 1])

    def testScalarDivision(self):
        """Тест деления на скаляр."""
        testPoly = Polynomial([4, 6, 8])
        resultPoly = testPoly / 2
        self.assertEqual(resultPoly.coefficients, [2, 3, 4])

    def testNegativeCoefficients(self):
        """Тест отрицательных коэффициентов."""
        testPoly = Polynomial([-2, 3, -1])
        self.assertEqual(testPoly(1), 0)
        self.assertEqual(testPoly(2), -3)

    def testLargePolynomial(self):
        """Тест многочлена высокой степени."""
        largePoly = Polynomial([1, 0, 0, 0, 0, 1])
        self.assertEqual(largePoly.degree, 5)
        self.assertEqual(largePoly(1), 2)

    def testPolynomialCopyIndependence(self):
        """Тест независимости копии."""
        originalPoly = Polynomial([1, 2, 3])
        copiedPoly = originalPoly.copy()

        # Изменение копии не должно влиять на оригинал
        copiedPoly._coefficients[0] = 999
        self.assertEqual(originalPoly.coefficients, [1, 2, 3])

    def testInheritanceRelationship(self):
        """Тест отношений наследования."""
        testPoly = Polynomial([1, 2, 3])
        self.assertIsInstance(testPoly, PolynomialBase)
        self.assertIsInstance(testPoly, Polynomial)

    def testOperationChain(self):
        """Тест цепочки операций."""
        polyFirst = Polynomial([2, -3, 1])
        polySecond = Polynomial([1, -1])
        polyThird = Polynomial([1, 1])

        resultPoly = (polyFirst + polySecond) * polyThird
        expectedPoly = Polynomial([2, 0, -2, 0])
        self.assertEqual(resultPoly.coefficients, expectedPoly.coefficients)

    def testDegreeCalculation(self):
        """Тест вычисления степени после операций."""
        polyFirst = Polynomial([1, 2, 3])
        polySecond = Polynomial([1, 1])

        sumResult = polyFirst + polySecond
        productResult = polyFirst * polySecond

        self.assertEqual(sumResult.degree, 2)
        self.assertEqual(productResult.degree, 3)

    def testEdgeCaseDivision(self):
        """Тест крайнего случая деления."""
        polyNumerator = Polynomial([1, 1])
        polyDenominator = Polynomial([1, 1])
        resultPoly = polyNumerator / polyDenominator
        self.assertEqual(resultPoly.coefficients, [1])

    def testFloatCoefficients(self):
        """Тест вещественных коэффициентов."""
        testPoly = Polynomial([1.5, 2.5, 3.5])
        self.assertEqual(testPoly(1), 7.5)
        self.assertEqual(testPoly(2), 14.5)

    def testNegativeDegreeAccess(self):
        """Тест доступа к отрицательной степени."""
        testPoly = Polynomial([1, 2, 3])
        self.assertEqual(testPoly[-1], 0)
        self.assertEqual(testPoly[10], 0)

    def testRepresentationMethod(self):
        """Тест метода repr."""
        testPoly = Polynomial([1, 2, 3])
        representationString = repr(testPoly)
        self.assertIn("polynomial_base", representationString)
        self.assertIn("[1, 2, 3]", representationString)

    def testComplexOperationSequence(self):
        """Тест сложной последовательности операций."""
        polyA = Polynomial([1, 1])
        polyB = Polynomial([2, 1])
        polyC = Polynomial([3, 1])
        resultPoly = (polyA * polyB) + (polyA * polyC) - polyA
        expectedPoly = Polynomial([5, 6, 1])  # 5x² + 6x + 1
        self.assertEqual(resultPoly.coefficients, expectedPoly.coefficients)

    def testPolynomialWithManyZeros(self):
        """Тест многочлена со многими нулями."""
        sparsePoly = Polynomial([0, 0, 0, 5, 0, 0, 3])
        self.assertEqual(sparsePoly.coefficients, [5, 0, 0, 3])
        self.assertEqual(sparsePoly.degree, 3)


if __name__ == '__main__':
    unittest.main()
