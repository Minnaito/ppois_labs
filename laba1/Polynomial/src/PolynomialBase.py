from .Constants import Constants


class PolynomialBase:

    def __init__(self, coefficients=None):

        self._constants = Constants()

        if coefficients is None:
            coefficients = self._constants.DEFAULT_COEFFICIENTS

        if isinstance(coefficients, (int, float)):
            coefficients = [coefficients]

        if not isinstance(coefficients, list):
            raise TypeError(self._constants.ERROR_INVALID_COEFFICIENTS)

        self._coefficients = self._remove_leading_zeros(coefficients)
        self._degree = len(self._coefficients) - self._constants.MIN_LENGTH

    def _remove_leading_zeros(self, coefficients):
        coefficients_copy = coefficients.copy()

        while (len(coefficients_copy) > self._constants.MIN_LENGTH and
               abs(coefficients_copy[self._constants.START_INDEX]) < self._constants.ZERO_THRESHOLD):
            coefficients_copy.pop(self._constants.START_INDEX)

        return coefficients_copy

    @property
    def coefficients(self):
        return self._coefficients.copy()

    @property
    def degree(self):
        return self._degree

    def __getitem__(self, index):
        if index < self._constants.START_INDEX or index > self._degree:
            return float(self._constants.DEFAULT_COEFFICIENT)
        return self._coefficients[index]

    def __call__(self, input_value):
        result_value = float(self._constants.DEFAULT_COEFFICIENT)
        for coefficient in self._coefficients:
            result_value = result_value * input_value + coefficient
        return result_value

    def __str__(self):
        if self._degree == self._constants.DEFAULT_COEFFICIENT:
            return str(self._coefficients[self._constants.START_INDEX])

        terms_list = []
        for index, coefficient in enumerate(self._coefficients):
            if abs(coefficient) < self._constants.ZERO_THRESHOLD:
                continue

            power_value = self._degree - index

            if power_value == self._constants.DEFAULT_COEFFICIENT:
                term_string = f"{coefficient:+g}"
            elif power_value == self._constants.MIN_LENGTH:
                term_string = f"{coefficient:+g}x"
            else:
                term_string = f"{coefficient:+g}x^{power_value}"

            if not terms_list and term_string.startswith('+'):
                term_string = term_string[self._constants.MIN_LENGTH:]
            terms_list.append(term_string)

        return ' '.join(terms_list) if terms_list else str(self._constants.DEFAULT_COEFFICIENT)

    def __repr__(self):
        return f"polynomial_base({self._coefficients})"

    def copy(self):
        return self.__class__(self._coefficients.copy())
