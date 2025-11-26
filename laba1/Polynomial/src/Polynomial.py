from .PolynomialBase import PolynomialBase
from .Constants import Constants


class Polynomial(PolynomialBase):

    def __add__(self, other):
        constantsObj = Constants()

        if isinstance(other, (int, float)):
            other = Polynomial([other])

        maxDegreeValue = max(self.degree, other.degree)
        resultCoefficients = [float(constantsObj.DEFAULT_COEFFICIENT)] * (maxDegreeValue + constantsObj.MIN_LENGTH)

        for currentIndex in range(maxDegreeValue + constantsObj.MIN_LENGTH):
            coefficientSelf = self[self.degree - currentIndex] if currentIndex <= self.degree else float(
                constantsObj.DEFAULT_COEFFICIENT)
            coefficientOther = other[other.degree - currentIndex] if currentIndex <= other.degree else float(
                constantsObj.DEFAULT_COEFFICIENT)
            resultCoefficients[currentIndex] = coefficientSelf + coefficientOther

        return Polynomial(resultCoefficients[::-constantsObj.MIN_LENGTH])

    def __iadd__(self, other):
        resultPolynomial = self + other
        self._coefficients = resultPolynomial._coefficients
        self._degree = resultPolynomial._degree
        return self

    def __sub__(self, other):
        constantsObj = Constants()

        if isinstance(other, (int, float)):
            other = Polynomial([other])

        maxDegreeValue = max(self.degree, other.degree)
        resultCoefficients = [float(constantsObj.DEFAULT_COEFFICIENT)] * (maxDegreeValue + constantsObj.MIN_LENGTH)

        for currentIndex in range(maxDegreeValue + constantsObj.MIN_LENGTH):
            coefficientSelf = self[self.degree - currentIndex] if currentIndex <= self.degree else float(
                constantsObj.DEFAULT_COEFFICIENT)
            coefficientOther = other[other.degree - currentIndex] if currentIndex <= other.degree else float(
                constantsObj.DEFAULT_COEFFICIENT)
            resultCoefficients[currentIndex] = coefficientSelf - coefficientOther

        return Polynomial(resultCoefficients[::-constantsObj.MIN_LENGTH])

    def __isub__(self, other):
        resultPolynomial = self - other
        self._coefficients = resultPolynomial._coefficients
        self._degree = resultPolynomial._degree
        return self

    def __mul__(self, other):
        constantsObj = Constants()

        if isinstance(other, (int, float)):
            resultCoefficients = [coefficient * other for coefficient in self._coefficients]
            return Polynomial(resultCoefficients)

        resultDegreeValue = self._degree + other._degree
        resultCoefficients = [float(constantsObj.DEFAULT_COEFFICIENT)] * (
                    resultDegreeValue + constantsObj.MIN_LENGTH)

        for outerIndex in range(self._degree + constantsObj.MIN_LENGTH):
            for innerIndex in range(other._degree + constantsObj.MIN_LENGTH):
                resultCoefficients[outerIndex + innerIndex] += self._coefficients[outerIndex] * other._coefficients[
                    innerIndex]

        return Polynomial(resultCoefficients)

    def __imul__(self, other):
        resultPolynomial = self * other
        self._coefficients = resultPolynomial._coefficients
        self._degree = resultPolynomial._degree
        return self

    def __truediv__(self, other):
        constantsObj = Constants()

        if isinstance(other, (int, float)):
            if abs(other) < constantsObj.ZERO_THRESHOLD:
                raise ZeroDivisionError(constantsObj.ERROR_DIVISION_BY_ZERO)
            resultCoefficients = [coefficient / other for coefficient in self._coefficients]
            return Polynomial(resultCoefficients)

        if other._degree > self._degree:
            return Polynomial([constantsObj.DEFAULT_COEFFICIENT])

        dividendCoefficients = self._coefficients.copy()
        divisorCoefficients = other._coefficients
        quotientDegreeValue = self._degree - other._degree
        quotientCoefficients = [float(constantsObj.DEFAULT_COEFFICIENT)] * (
                    quotientDegreeValue + constantsObj.MIN_LENGTH)

        for divisionIndex in range(quotientDegreeValue + constantsObj.MIN_LENGTH):
            quotientCoefficient = dividendCoefficients[divisionIndex] / divisorCoefficients[
                constantsObj.START_INDEX]
            quotientCoefficients[divisionIndex] = quotientCoefficient

            for subtractionIndex in range(len(divisorCoefficients)):
                dividendCoefficients[divisionIndex + subtractionIndex] -= quotientCoefficient * \
                                                                             divisorCoefficients[subtractionIndex]

        return Polynomial(quotientCoefficients)

    def __itruediv__(self, other):
        resultPolynomial = self / other
        self._coefficients = resultPolynomial._coefficients
        self._degree = resultPolynomial._degree
        return self
