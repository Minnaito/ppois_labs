import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.polynomial_base import PolynomialBase
from src.polynomial import Polynomial


class TestComprehensive(unittest.TestCase):

    def test_polynomial_creation(self):
        """Тест создания многочлена."""
        test_polynomial = Polynomial([1, 2, 3])
        self.assertEqual(test_polynomial.coefficients, [1, 2, 3])
        self.assertEqual(test_polynomial.degree, 2)

    def test_zero_polynomial(self):
        """Тест нулевого многочлена."""
        zero_polynomial = Polynomial([0])
        self.assertEqual(zero_polynomial.degree, 0)
        self.assertEqual(zero_polynomial(5), 0)

    def test_constant_polynomial(self):
        """Тест константного многочлена."""
        constant_poly = Polynomial([7])
        self.assertEqual(constant_poly.degree, 0)
        self.assertEqual(constant_poly(10), 7)

    def test_leading_zeros_removal(self):
        """Тест удаления ведущих нулей."""
        polynomial_with_zeros = Polynomial([0, 0, 3, 2])
        self.assertEqual(polynomial_with_zeros.coefficients, [3, 2])
        self.assertEqual(polynomial_with_zeros.degree, 1)

    def test_polynomial_string_format(self):
        """Тест форматирования строки."""
        poly_one = Polynomial([1, -2, 1])
        self.assertEqual(str(poly_one), "1x^2 -2x +1")

        poly_two = Polynomial([-1, 0, 1])
        self.assertEqual(str(poly_two), "-1x^2 +1")

    def test_polynomial_evaluation(self):
        """Тест вычисления значения."""
        test_poly = Polynomial([2, -1, 3])
        self.assertEqual(test_poly(0), 3)
        self.assertEqual(test_poly(1), 4)
        self.assertEqual(test_poly(2), 9)

    def test_coefficient_access(self):
        """Тест доступа к коэффициентам."""
        test_poly = Polynomial([4, 3, 2, 1])
        self.assertEqual(test_poly[0], 4)
        self.assertEqual(test_poly[1], 3)
        self.assertEqual(test_poly[2], 2)
        self.assertEqual(test_poly[3], 1)

    def test_addition_commutative(self):
        """Тест коммутативности сложения."""
        poly_first = Polynomial([1, 2])
        poly_second = Polynomial([3, 4])
        result_one = poly_first + poly_second
        result_two = poly_second + poly_first
        self.assertEqual(result_one.coefficients, result_two.coefficients)

    def test_multiplication_commutative(self):
        """Тест коммутативности умножения."""
        poly_first = Polynomial([1, 2])
        poly_second = Polynomial([3, 4])
        result_one = poly_first * poly_second
        result_two = poly_second * poly_first
        self.assertEqual(result_one.coefficients, result_two.coefficients)

    def test_addition_associativity(self):
        """Тест ассоциативности сложения."""
        poly_first = Polynomial([1, 2])
        poly_second = Polynomial([3, 4])
        poly_third = Polynomial([5, 6])

        left_result = (poly_first + poly_second) + poly_third
        right_result = poly_first + (poly_second + poly_third)
        self.assertEqual(left_result.coefficients, right_result.coefficients)

    def test_multiplication_associativity(self):
        """Тест ассоциативности умножения."""
        poly_first = Polynomial([1, 1])
        poly_second = Polynomial([2, 1])
        poly_third = Polynomial([3, 1])

        left_result = (poly_first * poly_second) * poly_third
        right_result = poly_first * (poly_second * poly_third)
        self.assertEqual(left_result.coefficients, right_result.coefficients)

    def test_distributive_property(self):
        """Тест дистрибутивности."""
        poly_first = Polynomial([1, 2])
        poly_second = Polynomial([3, 4])
        poly_third = Polynomial([5, 6])

        left_side = poly_first * (poly_second + poly_third)
        right_side = (poly_first * poly_second) + (poly_first * poly_third)
        self.assertEqual(left_side.coefficients, right_side.coefficients)

    def test_identity_addition(self):
        """Тест сложения с нулевым многочленом."""
        test_poly = Polynomial([1, 2, 3])
        zero_poly = Polynomial([0])
        result_poly = test_poly + zero_poly
        self.assertEqual(result_poly.coefficients, test_poly.coefficients)

    def test_identity_multiplication(self):
        """Тест умножения на единичный многочлен."""
        test_poly = Polynomial([1, 2, 3])
        one_poly = Polynomial([1])
        result_poly = test_poly * one_poly
        self.assertEqual(result_poly.coefficients, test_poly.coefficients)

    def test_zero_multiplication(self):
        """Тест умножения на ноль."""
        test_poly = Polynomial([1, 2, 3])
        zero_poly = Polynomial([0])
        result_poly = test_poly * zero_poly
        self.assertEqual(result_poly.coefficients, [0])

    def test_division_by_higher_degree(self):
        """Тест деления на многочлен большей степени."""
        poly_numerator = Polynomial([1, 2])
        poly_denominator = Polynomial([1, 0, 1])
        result_poly = poly_numerator / poly_denominator
        self.assertEqual(result_poly.coefficients, [0])

    def test_exact_division(self):
        """Тест точного деления."""
        poly_numerator = Polynomial([1, 3, 3, 1])
        poly_denominator = Polynomial([1, 1])
        result_poly = poly_numerator / poly_denominator
        self.assertEqual(result_poly.coefficients, [1, 2, 1])

    def test_scalar_division(self):
        """Тест деления на скаляр."""
        test_poly = Polynomial([4, 6, 8])
        result_poly = test_poly / 2
        self.assertEqual(result_poly.coefficients, [2, 3, 4])

    def test_negative_coefficients(self):
        """Тест отрицательных коэффициентов."""
        test_poly = Polynomial([-2, 3, -1])
        self.assertEqual(test_poly(1), 0)
        self.assertEqual(test_poly(2), -3)

    def test_large_polynomial(self):
        """Тест многочлена высокой степени."""
        large_poly = Polynomial([1, 0, 0, 0, 0, 1])
        self.assertEqual(large_poly.degree, 5)
        self.assertEqual(large_poly(1), 2)

    def test_polynomial_copy_independence(self):
        """Тест независимости копии."""
        original_poly = Polynomial([1, 2, 3])
        copied_poly = original_poly.copy()

        # Изменение копии не должно влиять на оригинал
        copied_poly._coefficients[0] = 999
        self.assertEqual(original_poly.coefficients, [1, 2, 3])

    def test_inheritance_relationship(self):
        """Тест отношений наследования."""
        test_poly = Polynomial([1, 2, 3])
        self.assertIsInstance(test_poly, PolynomialBase)
        self.assertIsInstance(test_poly, Polynomial)

    def test_operation_chain(self):
        """Тест цепочки операций."""
        poly_first = Polynomial([2, -3, 1])
        poly_second = Polynomial([1, -1])
        poly_third = Polynomial([1, 1])

        result_poly = (poly_first + poly_second) * poly_third
        expected_poly = Polynomial([2, 0, -2, 0])
        self.assertEqual(result_poly.coefficients, expected_poly.coefficients)

    def test_degree_calculation(self):
        """Тест вычисления степени после операций."""
        poly_first = Polynomial([1, 2, 3])
        poly_second = Polynomial([1, 1])

        sum_result = poly_first + poly_second
        product_result = poly_first * poly_second

        self.assertEqual(sum_result.degree, 2)
        self.assertEqual(product_result.degree, 3)

    def test_edge_case_division(self):
        """Тест крайнего случая деления."""
        poly_numerator = Polynomial([1, 1])
        poly_denominator = Polynomial([1, 1])
        result_poly = poly_numerator / poly_denominator
        self.assertEqual(result_poly.coefficients, [1])

    def test_float_coefficients(self):
        """Тест вещественных коэффициентов."""
        test_poly = Polynomial([1.5, 2.5, 3.5])
        self.assertEqual(test_poly(1), 7.5)
        self.assertEqual(test_poly(2), 14.5)

    def test_negative_degree_access(self):
        """Тест доступа к отрицательной степени."""
        test_poly = Polynomial([1, 2, 3])
        self.assertEqual(test_poly[-1], 0)
        self.assertEqual(test_poly[10], 0)

    def test_representation_method(self):
        """Тест метода repr."""
        test_poly = Polynomial([1, 2, 3])
        representation_string = repr(test_poly)
        self.assertIn("polynomial_base", representation_string)
        self.assertIn("[1, 2, 3]", representation_string)

    def test_complex_operation_sequence(self):
        """Тест сложной последовательности операций."""
        poly_a = Polynomial([1, 1])
        poly_b = Polynomial([2, 1])
        poly_c = Polynomial([3, 1])
        result_poly = (poly_a * poly_b) + (poly_a * poly_c) - poly_a
        expected_poly = Polynomial([5, 6, 1])  # 5x² + 6x + 1
        self.assertEqual(result_poly.coefficients, expected_poly.coefficients)

    def test_polynomial_with_many_zeros(self):
        """Тест многочлена со многими нулями."""
        sparse_poly = Polynomial([0, 0, 0, 5, 0, 0, 3])
        self.assertEqual(sparse_poly.coefficients, [5, 0, 0, 3])
        self.assertEqual(sparse_poly.degree, 3)


if __name__ == '__main__':
    unittest.main()
