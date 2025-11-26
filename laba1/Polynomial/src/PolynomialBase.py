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

        self._coefficients = self._removeLeadingZeros(coefficients)
        self._degree = len(self._coefficients) - self._constants.MIN_LENGTH

    def _removeLeadingZeros(self, coefficients):
        coefficientsCopy = coefficients.copy()

        while (len(coefficientsCopy) > self._constants.MIN_LENGTH and
               abs(coefficientsCopy[self._constants.START_INDEX]) < self._constants.ZERO_THRESHOLD):
            coefficientsCopy.pop(self._constants.START_INDEX)

        return coefficientsCopy

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

    def __call__(self, inputValue):
        resultValue = float(self._constants.DEFAULT_COEFFICIENT)
        for coefficient in self._coefficients:
            resultValue = resultValue * inputValue + coefficient
        return resultValue

    def __str__(self):
        if self._degree == self._constants.DEFAULT_COEFFICIENT:
            return str(self._coefficients[self._constants.START_INDEX])

        termsList = []
        for index, coefficient in enumerate(self._coefficients):
            if abs(coefficient) < self._constants.ZERO_THRESHOLD:
                continue

            powerValue = self._degree - index

            if powerValue == self._constants.DEFAULT_COEFFICIENT:
                termString = f"{coefficient:+g}"
            elif powerValue == self._constants.MIN_LENGTH:
                termString = f"{coefficient:+g}x"
            else:
                termString = f"{coefficient:+g}x^{powerValue}"

            if not termsList and termString.startswith('+'):
                termString = termString[self._constants.MIN_LENGTH:]
            termsList.append(termString)

        return ' '.join(termsList) if termsList else str(self._constants.DEFAULT_COEFFICIENT)

    def __repr__(self):
        return f"PolynomialBase({self._coefficients})"

    def copy(self):
        return self.__class__(self._coefficients.copy())
