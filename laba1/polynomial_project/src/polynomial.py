from .polynomial_base import polynomial_base
from .constants import constants


class polynomial(polynomial_base):

    def __add__(self, other):
        constants_obj = constants()

        if isinstance(other, (int, float)):
            other = polynomial([other])

        max_degree_value = max(self.degree, other.degree)
        result_coefficients = [float(constants_obj.DEFAULT_COEFFICIENT)] * (max_degree_value + constants_obj.MIN_LENGTH)

        for current_index in range(max_degree_value + constants_obj.MIN_LENGTH):
            coefficient_self = self[self.degree - current_index] if current_index <= self.degree else float(
                constants_obj.DEFAULT_COEFFICIENT)
            coefficient_other = other[other.degree - current_index] if current_index <= other.degree else float(
                constants_obj.DEFAULT_COEFFICIENT)
            result_coefficients[current_index] = coefficient_self + coefficient_other

        return polynomial(result_coefficients[::-constants_obj.MIN_LENGTH])

    def __iadd__(self, other):
        result_polynomial = self + other
        self._coefficients = result_polynomial._coefficients
        self._degree = result_polynomial._degree
        return self

    def __sub__(self, other):
        constants_obj = constants()

        if isinstance(other, (int, float)):
            other = polynomial([other])

        max_degree_value = max(self.degree, other.degree)
        result_coefficients = [float(constants_obj.DEFAULT_COEFFICIENT)] * (max_degree_value + constants_obj.MIN_LENGTH)

        for current_index in range(max_degree_value + constants_obj.MIN_LENGTH):
            coefficient_self = self[self.degree - current_index] if current_index <= self.degree else float(
                constants_obj.DEFAULT_COEFFICIENT)
            coefficient_other = other[other.degree - current_index] if current_index <= other.degree else float(
                constants_obj.DEFAULT_COEFFICIENT)
            result_coefficients[current_index] = coefficient_self - coefficient_other

        return polynomial(result_coefficients[::-constants_obj.MIN_LENGTH])

    def __isub__(self, other):
        result_polynomial = self - other
        self._coefficients = result_polynomial._coefficients
        self._degree = result_polynomial._degree
        return self

    def __mul__(self, other):
        constants_obj = constants()

        if isinstance(other, (int, float)):
            result_coefficients = [coefficient * other for coefficient in self._coefficients]
            return polynomial(result_coefficients)

        result_degree_value = self._degree + other._degree
        result_coefficients = [float(constants_obj.DEFAULT_COEFFICIENT)] * (
                    result_degree_value + constants_obj.MIN_LENGTH)

        for outer_index in range(self._degree + constants_obj.MIN_LENGTH):
            for inner_index in range(other._degree + constants_obj.MIN_LENGTH):
                result_coefficients[outer_index + inner_index] += self._coefficients[outer_index] * other._coefficients[
                    inner_index]

        return polynomial(result_coefficients)

    def __imul__(self, other):
        result_polynomial = self * other
        self._coefficients = result_polynomial._coefficients
        self._degree = result_polynomial._degree
        return self

    def __truediv__(self, other):
        constants_obj = constants()

        if isinstance(other, (int, float)):
            if abs(other) < constants_obj.ZERO_THRESHOLD:
                raise ZeroDivisionError(constants_obj.ERROR_DIVISION_BY_ZERO)
            result_coefficients = [coefficient / other for coefficient in self._coefficients]
            return polynomial(result_coefficients)

        if other._degree > self._degree:
            return polynomial([constants_obj.DEFAULT_COEFFICIENT])

        dividend_coefficients = self._coefficients.copy()
        divisor_coefficients = other._coefficients
        quotient_degree_value = self._degree - other._degree
        quotient_coefficients = [float(constants_obj.DEFAULT_COEFFICIENT)] * (
                    quotient_degree_value + constants_obj.MIN_LENGTH)

        for division_index in range(quotient_degree_value + constants_obj.MIN_LENGTH):
            quotient_coefficient = dividend_coefficients[division_index] / divisor_coefficients[
                constants_obj.START_INDEX]
            quotient_coefficients[division_index] = quotient_coefficient

            for subtraction_index in range(len(divisor_coefficients)):
                dividend_coefficients[division_index + subtraction_index] -= quotient_coefficient * \
                                                                             divisor_coefficients[subtraction_index]

        return polynomial(quotient_coefficients)

    def __itruediv__(self, other):
        result_polynomial = self / other
        self._coefficients = result_polynomial._coefficients
        self._degree = result_polynomial._degree
        return self
